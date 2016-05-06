from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from dwitter.models import Dweet
from dwitter.models import Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def comment(request, dweet_id):
  reply_to = get_object_or_404(Dweet, id=dweet_id) 
  c = Comment(text = request.POST['text']
      , reply_to = reply_to
      , author = request.user 
      , posted = timezone.now() )
  c.save()
  return HttpResponseRedirect(reverse('root'))
