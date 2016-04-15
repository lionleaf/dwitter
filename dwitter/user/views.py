from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from dwitter.models import Dweet
from django.contrib.auth.models import User

def user_feed(request, url_username, page_nr):
  user = get_object_or_404(User, username=url_username) 
  page = int(page_nr)
  dweets_per_page = 5
  first = (page - 1) * dweets_per_page
  last = page * dweets_per_page
  dweet_count = Dweet.objects.filter(author=user).count()

  if(first < 0 or first >= dweet_count):
    return render(request, 'base.html', {'text': 'No dweets here'});
  if(last >= dweet_count ):
    last = dweet_count;
  
  dweet_list = Dweet.objects.filter(author=user).order_by('-posted')[first:last]
  context = {'dweet_list': dweet_list
            ,'header_title': url_username
            ,'page_nr': page
            ,'next_url': reverse('user_feed_page', kwargs={
                                        'url_username': url_username,
                                        'page_nr': page + 1})
            ,'prev_url': reverse('user_feed_page', kwargs={
                                        'url_username': url_username,
                                        'page_nr': page - 1})
            }
  return render(request, 'feed/feed.html', context );
