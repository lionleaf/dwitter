from django.shortcuts import get_object_or_404, render
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

@login_required
def like(request, post_id):
  dweet = get_object_or_404(Dweet, id=post_id) 
  dweet.likes.add(request.user)
  dweet.save()
  return HttpResponseRedirect(reverse('feed'))
