from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.db.models import Count
from ..models import Dweet, Hashtag
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from functools import wraps
from datetime import datetime
from math import log
from django.contrib import messages
from django.utils.safestring import mark_safe
import json


def new_dweet_message(request, dweet_id):
    link = reverse('dweet_show',
                   kwargs={'dweet_id': dweet_id})
    furl = request.build_absolute_uri(link)
    messages.add_message(request, messages.SUCCESS,
                         mark_safe("Awesome dweet! "
                                   + "Use <a href='"
                                   + link + "'>" + furl + "</a>"
                                   + " to share it."))


def epoch_seconds(date):
    epoch = datetime(2015, 5, 5)
    naive = date.replace(tzinfo=None)
    td = naive - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def hot(likes, date):
    order = log(max(abs(likes), 1), 2)
    return round(order + epoch_seconds(date)/86400, 7)


def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        json_resp = json.dumps({'not_authenticated': True})
        return HttpResponse(json_resp, content_type='application/json')
    return wrapper


def feed(request, page_nr, sort):
    page = int(page_nr)
    dweets_per_page = 10
    first = (page - 1) * dweets_per_page
    last = page * dweets_per_page
    dweet_count = Dweet.objects.count()

    if(first < 0 or first > dweet_count):
        raise Http404("No such page")
    if(last >= dweet_count):
        last = dweet_count

    if (sort == "hot"):
        dweet_list = (Dweet.objects.annotate(num_likes=Count('likes'))
                      .order_by('-hotness', '-posted')[first:last])
        next_url = reverse('hot_feed_page', kwargs={'page_nr': page + 1})
        prev_url = reverse('hot_feed_page', kwargs={'page_nr': page - 1})
        # Main page title:
        title = "Dwitter  - javascript demos in 140 characters"
    elif(sort == "top"):
        dweet_list = (Dweet.objects.annotate(num_likes=Count('likes'))
                      .order_by('-num_likes', '-posted')[first:last])

        next_url = reverse('top_feed_page', kwargs={'page_nr': page + 1})
        prev_url = reverse('top_feed_page', kwargs={'page_nr': page - 1})
        title = "Top dweets | Dwitter"
    elif (sort == "new"):
        dweet_list = Dweet.objects.annotate(
            num_likes=Count('likes')).order_by('-posted')[first:last]
        next_url = reverse('new_feed_page', kwargs={'page_nr': page + 1})
        prev_url = reverse('new_feed_page', kwargs={'page_nr': page - 1})
        title = "New dweets | Dwitter"
    elif (sort == "random"):
        dweet_list = Dweet.objects.all().order_by('?')[:last-first]
        next_url = reverse('random_feed_page', kwargs={'page_nr': page + 1})
        prev_url = reverse('random_feed_page', kwargs={'page_nr': page - 1})
        title = "Random dweets | Dwitter"
    else:
        raise Http404("No such sorting method " + sort)

    dweet_list = list(
        dweet_list
        .select_related('author')
        .select_related('reply_to')
        .select_related('reply_to__author__username')
        .prefetch_related('comments'))

    # For some reason order_by('?') and .annotate(num_likes=Count('likes'))
    # don't work together, so we need to do extra work if the sorting is
    # random.
    if sort == 'random':
        for dweet in dweet_list:
            dweet.num_likes = dweet.likes.count()

    context = {'dweet_list': dweet_list,
               'feed_type': 'all',
               'title': title,
               'page_nr': page,
               'on_last_page': last == dweet_count,
               'next_url': next_url,
               'prev_url': prev_url,
               'sort': sort,
               'show_submit_box': True
               }
    return render(request, 'feed/feed.html', context)


def view_hashtag(request, page_nr, hashtag_name):
    hashtag = get_object_or_404(Hashtag.objects.all(), name=hashtag_name.lower())
    page = int(page_nr)
    dweets_per_page = 10
    first = (page - 1) * dweets_per_page
    last = page * dweets_per_page

    dweet_count = hashtag.dweets.count()

    if(first < 0 or first > dweet_count):
        raise Http404("No such page")
    if(last >= dweet_count):
        last = dweet_count

    title = "#" + hashtag_name + " tagged dweets | Dwitter"

    dweet_list = hashtag.dweets.annotate(num_likes=Count('likes')).order_by('-posted')[first:last]
    next_url = reverse('view_hashtag_page',
                       kwargs={'hashtag_name': hashtag_name, 'page_nr': page + 1})
    prev_url = reverse('view_hashtag_page',
                       kwargs={'hashtag_name': hashtag_name, 'page_nr': page - 1})

    dweet_list = list(
        dweet_list
        .select_related('author')
        .select_related('reply_to')
        .select_related('reply_to__author__username')
        .prefetch_related('comments'))

    context = {'dweet_list': dweet_list,
               'feed_type': 'hashtag',
               'title': title,
               'hashtag': hashtag_name,
               'page_nr': page,
               'on_last_page': last == dweet_count,
               'next_url': next_url,
               'prev_url': prev_url,
               'show_submit_box': True
               }
    return render(request, 'feed/feed.html', context)


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
    code = request.POST['code']

    if(len(code.replace('\r\n', '\n')) > 140):
        return HttpResponseBadRequest("Dweet code too long! Code: " + code)

    d = Dweet(code=code,
              author=request.user,
              posted=timezone.now())
    d.save()
    d.likes.add(d.author)
    d.hotness = hot(1, d.posted)
    d.save()

    new_dweet_message(request, d.id)

    return HttpResponseRedirect(reverse('dweet_show',
                                kwargs={'dweet_id': d.id}))


@login_required
def dweet_reply(request, dweet_id):
    reply_to = get_object_or_404(Dweet, id=dweet_id)
    d = Dweet(code=request.POST['code'],
              reply_to=reply_to,
              author=request.user,
              posted=timezone.now())
    d.save()
    d.likes.add(d.author)
    d.hotness = hot(1, d.posted)
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
    dweet.hotness = hot(likes, dweet.posted)
    dweet.save()
    json_resp = json.dumps({'likes': likes, 'liked': liked})
    return HttpResponse(json_resp, content_type='application/json')
