from dwitter.models import Comment, Dweet, Hashtag
from django.shortcuts import render
from dwitter.permissions import IsAuthorOrReadOnly
from dwitter.serializers import CommentSerializer, DweetSerializer
from dwitter.serializers import UserSerializer
from django.utils import timezone
from django.contrib.auth.models import User
from django_filters import FilterSet, NumberFilter, CharFilter
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets, mixins, permissions
from rest_framework.pagination import LimitOffsetPagination

from rest_framework_json_api.views import ModelViewSet, RelationshipView

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
class DweetViewSet(ModelViewSet):
    queryset = Dweet.objects.all()
    serializer_class = DweetSerializer
    
class HashtagViewSet(ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = DweetSerializer
    
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    multiple_lookup_fields = ['pk','username']

'''
class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = LimitOffsetPagination
    default_limit = 10
    queryset = Comment.objects.all()
    queryset = queryset.select_related('author').prefetch_related('reply_to')
    serializer_class = CommentSerializer
    filter_fields = ('reply_to', 'author')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, posted=timezone.now())
'''

class DweetFilterSet(FilterSet):
    remix_of = NumberFilter(field_name='reply_to')
    author = CharFilter(field_name='author__username')

    class Meta:
        model = Dweet
        fields = ['remix_of', 'author']

'''
class DweetViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Dweet.objects.all()
    queryset = queryset.select_related('author')
    queryset = queryset.prefetch_related('likes')
    filter_class = DweetFilterSet
    serializer_class = DweetSerializer
'''



'''
class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
'''