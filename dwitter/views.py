from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from dwitter.models import Dweet
from dwitter.models import Comment
from dwitter.serializers import CommentSerializer, DweetSerializer, UserSerializer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response


@login_required
def comment(request, dweet_id):
  reply_to = get_object_or_404(Dweet, id=dweet_id) 
  c = Comment(text = request.POST['comment-text']
      , reply_to = reply_to
      , author = request.user 
      , posted = timezone.now() )
  c.save()
  return HttpResponseRedirect(reverse('root'))

class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  filter_fields = ('reply_to', 'author')


  def perform_create(self, serializer):
    serializer.save(author=self.request.user, posted=timezone.now())

class DweetViewSet(viewsets.ModelViewSet):
  queryset = Dweet.objects.all()
  serializer_class = DweetSerializer

  def perform_create(self, serializer):
    serializer.save(author=self.request.user, posted=timezone.now())

  @detail_route()
  def comments(self, request, pk):
    dweet = get_object_or_404(Dweet, id=pk)
    c = Comment.objects.filter(reply_to=dweet).order_by('-posted')
    serializer = CommentSerializer(c, many = True)
    return Response(serializer.data)
