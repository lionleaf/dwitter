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

class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all()
  serializer_class = CommentSerializer
  filter_fields = ('reply_to', 'author')

  def perform_create(self, serializer):
    serializer.save(author=self.request.user, posted=timezone.now())
