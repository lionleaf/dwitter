import datetime

from dateutil.parser import parse
from django.contrib.auth.models import User
from django.db.models import Prefetch, Count
from django.utils import timezone
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from dwitter.webhooks import Webhooks
from dwitter.models import Comment, Dweet
from dwitter.serializers_v2 import DweetSerializer, UserSerializer
from dwitter.serializers_v2 import SetEmailSerializer, SetPasswordSerializer
from dwitter.utils import length_of_code


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

    @action(detail=True, methods=['POST'])
    def set_email(self, request, pk=None):
        user = self.get_object()
        if user != self.request.user:
            raise PermissionDenied()
        serializer = SetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.email = serializer.validated_data['email']
        user.save()
        context = self.get_serializer_context()
        return Response(UserSerializer(context=context).to_representation(user))

    @action(detail=True, methods=['POST'])
    def set_password(self, request, pk=None):
        user = self.get_object()
        context = self.get_serializer_context()
        if user != self.request.user:
            raise PermissionDenied()
        serializer = SetPasswordSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(context=context).to_representation(user))


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
        code = request.data.get('code', '')
        if (length_of_code(code) > 140):
            raise ValidationError("Code longer than 140 characters")

        remix_of_pk = request.data.get('remix_of', -1)

        # Using filter().first() will return None if it doesn't exist
        # instead of raising a DoesNotExist exception
        remix_of = self.queryset.filter(pk=remix_of_pk).first()

        d = Dweet(code=code,
                  author=request.user,
                  reply_to=remix_of,
                  posted=timezone.now())
        d.save()
        d.likes.add(d.author)
        d.save()

        first_comment = request.data.get('first-comment', '')
        if first_comment:
            c = Comment(text=first_comment,
                        posted=timezone.now(),
                        author=request.user,
                        reply_to=d)
            c.save()

        context = self.get_serializer_context()
        return Response(DweetSerializer(context=context).to_representation(d))

    def list(self, request):
        order_by = request.query_params.get('order_by', '-hotness')
        if order_by not in ('hotness', '-hotness', 'posted', '-posted', '-awesome_count', '?'):
            order_by = '-hotness'

        try:
            posted_before = parse(request.query_params.get('posted_before', ''))
        except ValueError:
            posted_before = datetime.datetime(year=9999, month=12, day=31)
        try:
            posted_after = parse(request.query_params.get('posted_after', ''))
        except ValueError:
            posted_after = datetime.datetime(year=1, month=1, day=1)

        username = request.query_params.get('username', None)
        hashtag = request.query_params.get('hashtag', None)
        filters = {}
        if username:
            filters['author__username'] = username
        if hashtag:
            filters['hashtag__name'] = hashtag

        if order_by == '-awesome_count':
            self.queryset = self.queryset.annotate(awesome_count=Count('likes'))

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

    @action(methods=['POST'], detail=True)
    def report(self, request, pk=None):
        if not request.user.is_authenticated:
            return PermissionDenied()

        dweet = self.get_object()
        result = Webhooks.send_mod_chat_message('[u/%s](https://www.dwitter.net/u/%s) reported [d/%s](https://www.dwitter.net/d/%s)' % (  # noqa: E501
            request.user.username,
            request.user.username,
            dweet.id,
            dweet.id,
        ))

        content = {'success': result}
        return_code = status.HTTP_200_OK
        if not result:
            return_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(content, status=return_code)
