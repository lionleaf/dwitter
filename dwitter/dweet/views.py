from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from dwitter.models import Dweet

def fullscreen_dweet(request, dweet_id):
  dweet = get_object_or_404(Dweet, id=dweet_id) 

  context = {'dweet': dweet
            }
  return render(request, 'dweet/dweet-id.html', context );
