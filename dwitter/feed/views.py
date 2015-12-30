from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from dwitter.models import Dweet
from django.contrib.auth.decorators import login_required

def feed(request):
  dweet_list = Dweet.objects.order_by('-posted')[:5]
  context = {'dweet_list': dweet_list
            ,'header_title': 'Global feed'}
  return render(request, 'feed/feed.html', context );


from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def dweet(request):
  d = Dweet(code = request.POST['code']
      , author = request.user 
      , posted = timezone.now() )
  d.save()
  return HttpResponseRedirect(reverse('feed'))
