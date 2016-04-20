from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from dwitter.models import Dweet
from django.contrib.auth.models import User

def user_feed(request, url_username, page_nr, sort):
  user = get_object_or_404(User, username=url_username) 
  page = int(page_nr)
  dweets_per_page = 10
  first = (page - 1) * dweets_per_page
  last = page * dweets_per_page
  dweet_count = Dweet.objects.filter(author=user).count()

  if(first < 0 or first >= dweet_count):
    return render(request, 'base.html', {'text': 'No dweets here'});
  if(last >= dweet_count ):
    last = dweet_count;

  dweet_list = Dweet.objects.filter(author=user)

  if(sort == "top"): 
    dweet_list = dweet_list.annotate(num_likes=Count('likes')).order_by('-num_likes')[first:last];
  elif (sort == "new"):
    dweet_list = dweet_list.order_by('-posted')[first:last];
  elif (sort == "hot"):
    dweet_list = dweet_list.annotate(num_likes=Count('likes')).order_by('-num_likes')[first:last];
  else:
    raise Http404("No such sorting method " + sort)

  next_url =  reverse('user_feed_page', kwargs={'url_username': url_username, 'page_nr': page + 1, 'sort': sort})
  prev_url =  reverse('user_feed_page', kwargs={'url_username': url_username, 'page_nr': page - 1, 'sort': sort})

  context = {'dweet_list': dweet_list
      ,'header_title': url_username
      ,'page_nr': page
      ,'next_url': next_url 
      ,'prev_url': prev_url
      }
  return render(request, 'feed/feed.html', context );
