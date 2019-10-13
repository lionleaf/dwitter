from dwitter.models import Comment, Dweet
from django.shortcuts import render
from dwitter.permissions import IsAuthorOrReadOnly
from dwitter.serializers import CommentSerializer, DweetSerializer
from dwitter.serializers import UserSerializer
from django.utils import timezone
from django.contrib.auth.models import User
from django_filters import FilterSet, NumberFilter, CharFilter
from rest_framework import viewsets, mixins, permissions
from rest_framework.pagination import LimitOffsetPagination


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


class DweetFilterSet(FilterSet):
    remix_of = NumberFilter(field_name='reply_to')
    author = CharFilter(field_name='author__username')

    class Meta:
        model = Dweet
        fields = ['remix_of', 'author']


class DweetViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Dweet.objects.all()
    queryset = queryset.select_related('author')
    queryset = queryset.prefetch_related('likes')
    filter_class = DweetFilterSet
    serializer_class = DweetSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


def about(request):
    return render(request, 'about.html', {'show_submit_box': True})
