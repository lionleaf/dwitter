from dateutil.parser import parse
from django.contrib.auth.models import User

from django.db.models import Prefetch, Count
from django.db.models.expressions import Exists, OuterRef
from django.utils import timezone

from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView

from dwitter.webhooks import Webhooks
from dwitter.models import Comment, Dweet
from dwitter.serializers_v2 import DweetSerializer, UserSerializer
from dwitter.serializers_v2 import SetEmailSerializer, SetPasswordSerializer
from dwitter.utils import length_of_code


class UserViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # POST action to create new user need to be available to everyone
        if self.request.method == 'POST' and self.action == 'create':
            self.permission_classes = (AllowAny,)

        return super(UserViewSet, self).get_permissions()

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
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Dweet.objects.all().select_related(
        'author',
        'reply_to',
        'reply_to__author'
    ).prefetch_related(
        Prefetch('remixes'),
        Prefetch('comments', queryset=Comment.objects.select_related('author'))
    ).annotate(
        awesome_count=Count('likes')
    ).order_by('-hotness')

    serializer_class = DweetSerializer

    def retrieve(self, request, pk):
        # For single dweet view, also include deleted dweets
        dweet = Dweet.with_deleted.select_related(
            'author',
            'reply_to',
            'reply_to__author'
        ).prefetch_related(
            Prefetch('remixes'),
            Prefetch('comments', queryset=Comment.objects.select_related('author'))
        ).annotate(
            awesome_count=Count('likes'),
            has_user_awesomed=Exists(Dweet.objects.filter(
                id=OuterRef('id'), likes__in=[request.user.id]))
        ).get(id=pk)

        context = self.get_serializer_context()
        return Response(DweetSerializer(context=context).to_representation(dweet))

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

        return self.retrieve(request, d.id)

    def list(self, request):
        order_by = request.query_params.get('order_by', '-hotness')
        if order_by not in ('hotness', '-hotness', 'posted', '-posted', '-awesome_count', '?'):
            order_by = '-hotness'

        try:
            posted_before = parse(request.query_params.get('posted_before', ''))
        except ValueError:
            posted_before = timezone.datetime(year=9999, month=12, day=31, tzinfo=timezone.utc)
        try:
            posted_after = parse(request.query_params.get('posted_after', ''))
        except ValueError:
            posted_after = timezone.datetime(year=1, month=1, day=1, tzinfo=timezone.utc)

        username = request.query_params.get('username', None)
        hashtag = request.query_params.get('hashtag', None)
        filters = {}
        if username:
            filters['author__username'] = username
        if hashtag:
            filters['hashtag__name'] = hashtag

        self.queryset = self.queryset.annotate(
            has_user_awesomed=Exists(Dweet.objects.filter(
                id=OuterRef('id'), likes__in=[request.user.id]))
        )

        self.queryset = self.queryset.order_by(order_by).filter(
            posted__gte=posted_after, posted__lt=posted_before, **filters)

        return super().list(request)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()

        dweet = self.get_object()

        # Only allow deletion of own dweets
        # unless the deleter is a mod
        if request.user == dweet.author or request.user.is_staff:
            dweet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise PermissionDenied()

    @action(methods=['POST'], detail=True)
    def set_like(self, request, pk=None):
        if not request.user.is_authenticated:
            raise PermissionDenied()

        dweet = self.get_object()

        like = request.data.get('like', True)

        if like:
            dweet.likes.add(request.user)
        else:
            dweet.likes.remove(request.user)

        return self.retrieve(request, dweet.id)

    @action(methods=['POST'], detail=True)
    def add_comment(self, request, pk=None):
        if not request.user.is_authenticated:
            raise PermissionDenied()

        text = request.data.get('text', '')

        dweet = self.get_object()
        Comment.objects.create(
            reply_to=dweet, text=text, author=request.user, posted=timezone.now())

        return self.retrieve(request, dweet.id)

    @action(methods=['POST'], detail=True)
    def report(self, request, pk=None):
        if not request.user.is_authenticated:
            raise PermissionDenied()

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


class CommentViewSet(viewsets.GenericViewSet,
                     mixins.DestroyModelMixin):
    queryset = Comment.objects.all().select_related(
        'author',
    ).order_by('posted')
    serializer_class = DweetSerializer

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied()

        comment = self.get_object()

        # Only allow deletion of own dweets
        # unless the deleter is a mod
        if request.user == comment.author or request.user.is_staff:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        raise PermissionDenied()

    @action(methods=['POST'], detail=True)
    def report(self, request, pk=None):
        if not request.user.is_authenticated:
            raise PermissionDenied()

        comment = self.get_object()
        result = Webhooks.send_mod_chat_message('[u/%s](https://www.dwitter.net/u/%s) reported comment on'  # noqa: E501
                                                ' [d/%s](https://www.dwitter.net/d/%s)'
                                                ' by [u/%s](https://www.dwitter.net/u/%s):'
                                                ' "%s" (Comment id: %d)' % (
                                                    request.user.username, request.user.username,
                                                    comment.reply_to.pk, comment.reply_to.pk,
                                                    comment.author, comment.author,
                                                    comment.text, comment.pk)
                                                )
        content = {'success': result}
        return_code = status.HTTP_200_OK
        if not result:
            return_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return Response(content, status=return_code)


class StatsAPI(GenericAPIView):
    queryset = Dweet.objects.all()

    def get(self, _, **kwargs):
        username = kwargs.get('url_username')
        dweets = self.queryset.filter(author__username=username)
        stats = {
            'dweet_count': dweets.count(),
            'awesome_count': dweets.aggregate(Count('likes'))['likes__count'],
        }
        return Response(stats)
