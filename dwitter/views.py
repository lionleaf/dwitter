from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from dwitter.models import Dweet
from dwitter.models import Comment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
import json

@login_required
def comment(request, dweet_id):
  reply_to = get_object_or_404(Dweet, id=dweet_id) 
  c = Comment(text = request.POST['comment-text']
      , reply_to = reply_to
      , author = request.user 
      , posted = timezone.now() )
  c.save()
  return HttpResponseRedirect(reverse('root'))

def get_comments(request, dweet_id):
  dweet = get_object_or_404(Dweet, id=dweet_id)
  comments = Comment.objects.filter(reply_to=dweet).order_by('posted')
  comment_list = []
#TODO: Is there a better way to do this?
  for comment in comments:
    comment_list.append({'text':comment.text
                        #, 'posted': comment.posted
                        , 'author_id': comment.author.id
                        , 'author_username': comment.author.username})
  json_resp = json.dumps(comment_list)
  return HttpResponse(json_resp, content_type='application/json')
