from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.db.models import Count, Sum, Prefetch
from ..models import Dweet, Hashtag, Comment
from dwitter.utils import length_of_code
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from functools import wraps
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.generic import ListView
from ..webhooks import Webhooks
import json


def simple_discord_escape(text):
    for character in '`|[<*_~-=.1':
        text = text.replace(character, '\\' + character)
    return text


class SortMethod:
    NEW = {'ordering': ['-posted']}
    HOT = {'ordering': ['-hotness', '-posted']}
    TOP = {'ordering': ['-num_likes', '-posted']}
    RANDOM = {'ordering': ['?']}


class DweetFeed(ListView):
    sort = SortMethod.NEW  # default sort by new
    model = Dweet
    context_object_name = 'dweets'
    template_name = 'feed.html'
    paginate_by = 10
    title = "Dwitter"
    feed_type = "all"  # TODO: Find a better mechanism for this
    show_submit_box = True

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DweetFeed, self).get_context_data(**kwargs)
        # Add additional context data
        context['title'] = self.title
        context['feed_type'] = self.feed_type
        context['show_submit_box'] = self.show_submit_box
        context['feed_name'] = self.feed_name
        return context

    def get_queryset(self):
        queryset = self.get_dweet_list()
        queryset = queryset.order_by(*self.get_ordering())

        # Optimize the SQL query:
        prefetch_comments = Prefetch('comments', queryset=Comment.objects.select_related('author'))
        prefetch_replies = Prefetch('dweet_set', queryset=Dweet.objects.select_related('author'))
        queryset = (
            queryset
            .select_related('author')
            .prefetch_related(Prefetch('reply_to', queryset=Dweet.objects.select_related('author')))
            .prefetch_related('likes')
            .prefetch_related(prefetch_comments)
            .prefetch_related(prefetch_replies))

        return queryset

    def get_ordering(self):
        return self.sort['ordering']

    def get_dweet_list(self):
        raise  # should be implemented by all subclasses!


class AllDweetFeed(DweetFeed):
    """ Base class for the main dweet feeds that contains all dweets """

    def get_dweet_list(self):
        dweet_list = Dweet.objects
        return dweet_list


class HotDweetFeed(AllDweetFeed):
    title = "Dwitter  - javascript demos in 140 characters"
    sort = SortMethod.HOT
    feed_name = "hot"


class TopDweetFeedBase(DweetFeed):
    def get_dweet_list(self):
        date_cutoff = timezone.now() - timezone.timedelta(days=self.days)
        return Dweet.objects.filter(posted__gte=date_cutoff).annotate(num_likes=Count('likes'))

    def get_context_data(self, **kwargs):
        context = super(TopDweetFeedBase, self).get_context_data(**kwargs)
        context['top_name'] = self.top_name
        return context


class TopWeekDweetFeed(TopDweetFeedBase):
    title = "Top dweets this week | Dwitter"
    sort = SortMethod.TOP
    feed_name = "top-week"
    top_name = "week"
    days = 7


class TopMonthDweetFeed(TopDweetFeedBase):
    title = "Top dweets this month | Dwitter"
    sort = SortMethod.TOP
    feed_name = "top-month"
    top_name = "month"
    days = 30


class TopYearDweetFeed(TopDweetFeedBase):
    title = "Top dweets this year | Dwitter"
    sort = SortMethod.TOP
    feed_name = "top-year"
    top_name = "year"
    days = 365


class TopAllDweetFeed(AllDweetFeed):
    title = "Top dweets of all time | Dwitter"
    sort = SortMethod.TOP
    feed_name = "top-all"
    top_name = "all time"

    def get_context_data(self, **kwargs):
        context = super(TopAllDweetFeed, self).get_context_data(**kwargs)
        context['top_name'] = self.top_name
        return context

    def get_dweet_list(self):
        return Dweet.objects.annotate(num_likes=Count('likes'))


class NewDweetFeed(AllDweetFeed):
    title = "New dweets | Dwitter"
    sort = SortMethod.NEW
    feed_name = "new"


class RandomDweetFeed(AllDweetFeed):
    title = "Random dweets | Dwitter"
    sort = SortMethod.RANDOM
    feed_name = "random"


class HashtagFeed(DweetFeed):
    """
    Base class for the hashtag feeds.
    Should be subclassed for different sort methods
    """
    feed_type = 'hashtag'

    def get_context_data(self, **kwargs):
        self.title = self.get_title()
        context = super(HashtagFeed, self).get_context_data(**kwargs)
        context['hashtag'] = self.kwargs['hashtag_name']
        return context

    def get_dweet_list(self):
        hashtag_name = self.kwargs['hashtag_name']
        hashtag = get_object_or_404(Hashtag.objects.all(), name=hashtag_name.lower())
        queryset = hashtag.dweets
        return queryset


class NewHashtagFeed(HashtagFeed):
    sort = SortMethod.NEW
    feed_name = "new"

    def get_title(self):
        hashtag_name = self.kwargs['hashtag_name']
        return "New #" + hashtag_name + " dweets | Dwitter"


class TopHashtagFeed(HashtagFeed):
    sort = SortMethod.TOP
    feed_name = "top"

    def get_title(self):
        hashtag_name = self.kwargs['hashtag_name']
        return "Top #" + hashtag_name + " dweets | Dwitter"

    def get_dweet_list(self):
        return super().get_dweet_list().annotate(num_likes=Count('likes'))


class UserFeed(DweetFeed):
    """
    Base class for the user feeds.
    Should be subclassed for different sort methods
    """
    feed_type = 'user'

    def get_context_data(self):
        context = super(UserFeed, self).get_context_data()

        username = self.kwargs['url_username']
        user = get_object_or_404(User, username=username)
        total_awesome = self.get_queryset().aggregate(
            totalaws=Sum('num_likes'))['totalaws']

        context['title'] = self.get_title()
        context['user'] = user
        context['total_awesome'] = total_awesome or 0
        return context

    def get_dweet_list(self):
        username = self.kwargs['url_username']
        user = get_object_or_404(User, username=username)
        return Dweet.objects.filter(author=user).annotate(num_likes=Count('likes'))


class NewUserFeed(UserFeed):
    sort = SortMethod.NEW
    feed_name = "new"

    def get_title(self):
        return "Dweets by u/" + self.kwargs['url_username'] + " | Dwitter"


class TopUserFeed(UserFeed):
    sort = SortMethod.TOP
    feed_name = "top"

    def get_title(self):
        return "Top dweets by u/" + self.kwargs['url_username'] + " | Dwitter"


class HotUserFeed(UserFeed):
    sort = SortMethod.HOT
    feed_name = "hot"

    def get_title(self):
        return "Hot dweets by u/" + self.kwargs['url_username'] + " | Dwitter"


class LikedFeed(DweetFeed):
    """
    Base class for the list of dweets liked by a specific user
    Should be subclassed for different sort methods
    """
    feed_type = 'user'

    def get_context_data(self):
        context = super(LikedFeed, self).get_context_data()

        username = self.kwargs['url_username']
        user = get_object_or_404(User, username=username)
        total_awesome = self.get_queryset().aggregate(
            totalaws=Sum('num_likes'))['totalaws']

        context['title'] = self.get_title()
        context['user'] = user
        context['total_awesome'] = total_awesome or 0
        context['sort'] = 'awesome'
        return context

    def get_dweet_list(self):
        username = self.kwargs['url_username']
        user = get_object_or_404(User, username=username)
        # Seems to needs the annotate before filter in order to work
        queryset = Dweet.objects.annotate(num_likes=Count('likes')).filter(likes=user)
        return queryset


class NewLikedFeed(LikedFeed):
    sort = SortMethod.NEW
    feed_name = "awesome"

    def get_title(self):
        return "Dweets awesomed by u/" + self.kwargs['url_username'] + " | Dwitter"


def new_dweet_message(request, dweet_id):
    link = reverse('dweet_show',
                   kwargs={'dweet_id': dweet_id})
    furl = request.build_absolute_uri(link)
    messages.add_message(request, messages.SUCCESS,
                         mark_safe("Awesome dweet! "
                                   + "Use <a href='"
                                   + link + "'>" + furl + "</a>"
                                   + " to share it."))


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        json_resp = json.dumps({'not_authenticated': True})
        return HttpResponse(json_resp, content_type='application/json')
    return wrapper


def dweet_show(request, dweet_id):
    dweet = get_object_or_404(Dweet.with_deleted.annotate(
        num_likes=Count('likes')), id=dweet_id)

    context = {
        'dweet': dweet,
        'show_submit_box': True,
    }

    return render(request, 'feed/permalink.html', context)


@xframe_options_exempt
def dweet_embed(request, dweet_id):
    dweet = get_object_or_404(Dweet.with_deleted.annotate(
        num_likes=Count('likes')), id=dweet_id)
    context = {
        'dweet': dweet
    }

    return render(request, 'feed/embed.html', context)


@login_required
def dweet(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    code = request.POST['code']

    if(length_of_code(code) > 140):
        return HttpResponseBadRequest("Dweet code too long! Code: " + code)

    d = Dweet(code=code,
              author=request.user,
              posted=timezone.now())
    d.save()
    d.likes.add(d.author)
    d.save()

    first_comment = request.POST.get('first-comment', '')
    if first_comment:
        c = Comment(text=first_comment,
                    posted=timezone.now(),
                    author=request.user,
                    reply_to=d)
        c.save()

    new_dweet_message(request, d.id)

    return HttpResponseRedirect(reverse('dweet_show',
                                kwargs={'dweet_id': d.id}))


@login_required
def dweet_reply(request, dweet_id):
    if request.method != 'POST':
        return HttpResponse(status=405)

    code = request.POST['code']

    if(length_of_code(code) > 140):
        return HttpResponseBadRequest("Dweet code too long! Code: " + code)

    reply_to = get_object_or_404(Dweet, id=dweet_id)
    d = Dweet(code=code,
              reply_to=reply_to,
              author=request.user,
              posted=timezone.now())
    d.save()
    d.likes.add(d.author)
    d.save()

    first_comment = request.POST.get('first-comment', '')
    if first_comment:
        c = Comment(text=first_comment,
                    posted=timezone.now(),
                    author=request.user,
                    reply_to=d)
        c.save()

    new_dweet_message(request, d.id)

    return HttpResponseRedirect(reverse('dweet_show',
                                kwargs={'dweet_id': d.id}))


@csrf_protect
@login_required
@require_POST
def dweet_delete(request, dweet_id):
    dweet = get_object_or_404(Dweet, id=dweet_id)
    if(request.user == dweet.author or request.user.is_staff):
        dweet.delete()
        return HttpResponseRedirect(reverse('root'))

    return HttpResponse("Not authorized to delete the dweet.")


@ajax_login_required
@require_POST
def like(request, dweet_id):
    dweet = get_object_or_404(Dweet, id=dweet_id)

    if(dweet.likes.filter(id=request.user.id).exists()):
        liked = False
        dweet.likes.remove(request.user)
    else:
        liked = True
        dweet.likes.add(request.user)

    likes = dweet.likes.count()
    dweet.save()
    json_resp = json.dumps({'likes': likes, 'liked': liked})
    return HttpResponse(json_resp, content_type='application/json')


@ajax_login_required
@require_POST
def report_dweet(request, dweet_id):
    dweet = get_object_or_404(Dweet, id=dweet_id)
    Webhooks.send_mod_chat_message('[u/%s](https://www.dwitter.net/u/%s) reported [d/%s](https://www.dwitter.net/d/%s)' % (  # noqa: E501
        request.user.username,
        request.user.username,
        dweet.id,
        dweet.id,
    ))
    return HttpResponse('{"result": "OK"}', content_type='application/json')


@ajax_login_required
@require_POST
def report_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    Webhooks.send_mod_chat_message('[u/%s](https://www.dwitter.net/u/%s) reported a comment by [u/%s](https://www.dwitter.net/u/%s) on [d/%s](https://www.dwitter.net/d/%s).\nContents (click to reveal): || %s ||' % (  # noqa: E501
        request.user.username,
        request.user.username,
        comment.author.username,
        comment.author.username,
        comment.reply_to.id,
        comment.reply_to.id,
        simple_discord_escape(comment.text),
    ))
    return HttpResponse('{"result": "OK"}', content_type='application/json')
