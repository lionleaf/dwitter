from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from dwitter.models import Dweet

def feed(request):
    dweet_list = Dweet.objects.order_by('-posted')
    context = {'dweet_list': dweet_list}
    return render(request, 'feed/feed.html', context );


from django.contrib.auth.models import User
from django.utils import timezone

def dweet(request):
    d = Dweet(code = request.POST['code']
            , author = User.objects.get(username='lionleaf')
            , posted = timezone.now() )
    d.save()
    return HttpResponseRedirect(reverse('feed'))
