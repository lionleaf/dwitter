from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.db.models import Count
from dwitter.models import Dweet
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from functools import wraps
import json


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

    if(sort == "top"):
        dweet_list = (Dweet.objects.annotate(num_likes=Count('likes'))
                      .order_by('-num_likes', '-posted')[first:last])

        next_url = reverse('top_feed_page', kwargs={'page_nr': page + 1})
        prev_url = reverse('top_feed_page', kwargs={'page_nr': page - 1})
    elif (sort == "new"):
        dweet_list = Dweet.objects.order_by('-posted')[first:last]
        next_url = reverse('new_feed_page', kwargs={'page_nr': page + 1})
        prev_url = reverse('new_feed_page', kwargs={'page_nr': page - 1})
    elif (sort == "hot"):
        dweet_list = (Dweet.objects.annotate(num_likes=Count('likes'))
                      .order_by('-num_likes', '-posted')[first:last])
        next_url = reverse('hot_feed_page', kwargs={'page_nr': page + 1})
        prev_url = reverse('hot_feed_page', kwargs={'page_nr': page - 1})
    else:
        raise Http404("No such sorting method " + sort)

    context = {'dweet_list': dweet_list,
               'header_title': 'Dwitter',
               'feed_type': 'all',
               'page_nr': page,
               'next_url': next_url,
               'prev_url': prev_url,
               'sort': sort,
               }
    return render(request, 'feed/feed.html', context)


@login_required
def dweet(request):
    d = Dweet(code=request.POST['code'],
              author=request.user,
              posted=timezone.now())
    d.save()
    return HttpResponseRedirect(reverse('root'))


@login_required
def dweet_reply(request, dweet_id):
    reply_to = get_object_or_404(Dweet, id=dweet_id)
    d = Dweet(code=request.POST['code'],
              reply_to=reply_to,
              author=request.user,
              posted=timezone.now())
    d.save()
    return HttpResponseRedirect(reverse('root'))


@login_required
def dweet_delete(request):
    dweet_id = request.POST['dweet-id']
    dweet = get_object_or_404(Dweet, id=dweet_id)
    if(request.user == dweet.author or request.user.is_staff):
        dweet.delete()
        return HttpResponseRedirect(reverse('root'))

    return HttpResponse("Not authorized to delete the dweet.")


@ajax_login_required
def like(request, post_id):
    dweet = get_object_or_404(Dweet, id=post_id)

    if(dweet.likes.filter(id=request.user.id).exists()):
        liked = False
        dweet.likes.remove(request.user)
    else:
        liked = True
        dweet.likes.add(request.user)
    dweet.save()
    json_resp = json.dumps({'likes': dweet.likes.count(), 'liked': liked})
    return HttpResponse(json_resp, content_type='application/json')
