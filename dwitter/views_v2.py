import datetime

from dateutil.parser import parse
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from dwitter.models import Comment, Dweet
from dwitter.serializers_v2 import DweetSerializer, UserSerializer


class UserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        if self.kwargs['pk'] == 'me':
            if self.request.user.is_authenticated:
                return self.request.user
            else:
                raise PermissionDenied()
        return super().get_object()


class DweetViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Dweet.objects.all().select_related(
        'author',
    ).prefetch_related(
        'likes',
        Prefetch('comments', queryset=Comment.objects.select_related('author'))
    ).order_by('-hotness')
    serializer_class = DweetSerializer

    def create(self, request):
        from dwitter.feed.views import dweet as original_dweet_view

        class DummyRequest:
            def __init__(self):
                self.method = 'POST'
                self.POST = request.data
                self.build_absolute_uri = request.build_absolute_uri
                self._messages = request._messages
                self.META = request.META
                self.user = request.user

        response = original_dweet_view(DummyRequest())
        pk = int(response.url.split('/')[-1])
        dweet = self.queryset.get(pk=pk)
        context = self.get_serializer_context()
        return Response(DweetSerializer(context=context).to_representation(dweet))

    def list(self, request):
        order_by = request.query_params.get('order_by', '-hotness')
        if order_by not in ('hotness', '-hotness', 'posted', '-posted', '?'):
            order_by = '-hotness'
        try:
            posted_before = parse(request.query_params.get('posted_before', ''))
        except ValueError:
            posted_before = datetime.datetime(year=9999, month=12, day=31)
        try:
            posted_after = parse(request.query_params.get('posted_after', ''))
        except ValueError:
            posted_after = datetime.datetime(year=1, month=1, day=1)

        if order_by not in ('hotness', '-hotness', 'posted', '-posted', '?'):
            order_by = '-hotness'

        username = request.query_params.get('username', None)
        hashtag = request.query_params.get('hashtag', None)
        filters = {}
        if username:
            filters['author__username'] = username
        if hashtag:
            filters['hashtag__name'] = hashtag

        self.queryset = self.queryset.order_by(order_by).filter(
            posted__gte=posted_after, posted__lt=posted_before, **filters)

        return super().list(request)

    @action(methods=['POST'], detail=True)
    def set_like(self, request, pk=None):
        if not request.user.is_authenticated:
            return PermissionDenied()

        dweet = self.get_object()

        like = request.data.get('like', True)

        if like:
            dweet.likes.add(request.user)
        else:
            dweet.likes.remove(request.user)

        dweet = self.queryset.get(pk=dweet.pk)
        context = self.get_serializer_context()
        return Response(DweetSerializer(context=context).to_representation(dweet))

    @action(methods=['POST'], detail=True)
    def add_comment(self, request, pk=None):
        if not request.user.is_authenticated:
            return PermissionDenied()

        text = request.data.get('text', '')

        dweet = self.get_object()
        Comment.objects.create(
            reply_to=dweet, text=text, author=request.user, posted=timezone.now())

        dweet = self.queryset.get(pk=dweet.pk)
        context = self.get_serializer_context()
        return Response(DweetSerializer(context=context).to_representation(dweet))
