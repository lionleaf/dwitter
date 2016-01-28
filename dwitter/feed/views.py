from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from dwitter.models import Dweet
from django.contrib.auth.decorators import login_required

def feed(request, page_nr):
  page = int(page_nr)
  dweets_per_page = 10
  first = (page - 1) * dweets_per_page
  last = page * dweets_per_page
  dweet_count = Dweet.objects.count()

  if(first < 0 or first > dweet_count):
    raise Http404("No such page")
  if(last >= dweet_count ):
    last = dweet_count;
  
  dweet_list = Dweet.objects.order_by('-posted')[first:last]
  context = {'dweet_list': dweet_list
            ,'header_title': 'Global feed'
            ,'page_nr': page
            ,'next_url': reverse('feed', kwargs={'page_nr': page + 1})
            ,'prev_url': reverse('feed', kwargs={'page_nr': page - 1})
            }
  return render(request, 'feed/feed.html', context );


from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def dweet(request):
  d = Dweet(code = request.POST['code']
      , author = request.user 
      , posted = timezone.now() )
  d.save()
  return HttpResponseRedirect(reverse('root'))

@login_required
def like(request, post_id):
  dweet = get_object_or_404(Dweet, id=post_id) 
  dweet.likes.add(request.user)
  dweet.save()
  return HttpResponseRedirect(reverse('root'))
