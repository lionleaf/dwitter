from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from dwitter.models import Dweet
from django.contrib.auth.models import User

def user_feed(request, url_username):
  user = get_object_or_404(User, username=url_username) 
  dweet_list = Dweet.objects.filter(author=user).order_by('-posted')[:5]
  context = {'dweet_list': dweet_list
            ,'header_title': url_username + ' feed'}
  return render(request, 'feed/feed.html', context );
