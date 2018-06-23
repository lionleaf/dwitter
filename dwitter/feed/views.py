from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.db.models import Count
from ..models import Dweet, Hashtag
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from functools import wraps
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.views.generic import ListView
import json


class SortMethod:
    NEW = ['-posted']
    HOT = ['-hotness', '-posted']
    TOP = ['-num_likes', '-posted']
    RANDOM = ['?']


class DweetFeed(ListView):
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
        return context

    def get_queryset(self):
        queryset = self.get_dweet_list()
        queryset = queryset.order_by(*self.get_ordering())

        # Optimize the SQL query:
        queryset = (
            queryset
            .select_related('author')
            .select_related('reply_to')
            .select_related('reply_to__author__username')
            .prefetch_related('comments'))

        return queryset

    def get_dweet_list(self):
        raise  # should be implemented by all subclasses!


class AllDweetFeed(DweetFeed):
    """
    Base class for the main dweet feeds that contains all dweets
    """
    def get_dweet_list(self):
        dweet_list = (Dweet.objects.annotate(num_likes=Count('likes')))
        return dweet_list


class HotDweetFeed(AllDweetFeed):
    title = "Dwitter  - javascript demos in 140 characters"
    ordering = SortMethod.HOT


class TopDweetFeed(AllDweetFeed):
    title = "Top dweets | Dwitter"
    ordering = SortMethod.TOP


class NewDweetFeed(AllDweetFeed):
    title = "New dweets | Dwitter"
    ordering = SortMethod.NEW


class RandomDweetFeed(AllDweetFeed):
    title = "Random dweets | Dwitter"
    ordering = SortMethod.RANDOM


class HashtagFeed(DweetFeed):
    """
    Base class for the hashtag feeds.
    Should be subclassed for different sort methods
    """
    feed_type = 'hashtag'

    def get_context_data(self, **kwargs):
        self.title = self.get_title(**kwargs)
        context = super(DweetFeed, self).get_context_data(**kwargs)
        context['hashtag'] = self.kwargs['hashtag_name']
        return context

    def get_dweet_list(self):
        hashtag_name = self.kwargs['hashtag_name']
        hashtag = get_object_or_404(Hashtag.objects.all(), name=hashtag_name.lower())
        queryset = hashtag.dweets.annotate(num_likes=Count('likes'))
        return queryset


class NewHashtagFeed(HashtagFeed):
    ordering = SortMethod.NEW

    def get_title(self, **kwargs):
        hashtag_name = self.kwargs['hashtag_name']
        self.title = "New #" + hashtag_name + " dweets | Dwitter"


class TopHashtagFeed(HashtagFeed):
    ordering = ['-posted']

    def get_title(self, **kwargs):
        hashtag_name = self.kwargs['hashtag_name']
        self.title = "Top #" + hashtag_name + " dweets | Dwitter"


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
        if request.user.is_authenticated():
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

    if(len(code.replace('\r\n', '\n')) > 140):
        return HttpResponseBadRequest("Dweet code too long! Code: " + code)

    d = Dweet(code=code,
              author=request.user,
              posted=timezone.now())
    d.save()
    d.likes.add(d.author)
    d.save()

    new_dweet_message(request, d.id)

    return HttpResponseRedirect(reverse('dweet_show',
                                kwargs={'dweet_id': d.id}))


@login_required
def dweet_reply(request, dweet_id):
    if request.method != 'POST':
        return HttpResponse(status=405)

    code = request.POST['code']

    if(len(code.replace('\r\n', '\n')) > 140):
        return HttpResponseBadRequest("Dweet code too long! Code: " + code)

    reply_to = get_object_or_404(Dweet, id=dweet_id)
    d = Dweet(code=code,
              reply_to=reply_to,
              author=request.user,
              posted=timezone.now())
    d.save()
    d.likes.add(d.author)
    d.save()

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
