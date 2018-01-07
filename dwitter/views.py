from dwitter.models import Comment, Dweet
from dwitter.permissions import IsAuthorOrReadOnly
from dwitter.serializers import CommentSerializer, DweetSerializer
from django.utils import timezone
from rest_framework import viewsets, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route



class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fields = ('reply_to', 'author')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, posted=timezone.now())

class DweetViewSet( mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Dweet.objects.all()
    serializer_class = DweetSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, posted=timezone.now())

    @list_route()
    def newest(self, request):
        newest_dweet = Dweet.objects.latest(field_name='posted')
        serializer = self.get_serializer(newest_dweet)
        return Response(serializer.data)

    @detail_route()
    def remixes(self, request, pk=None):
        remix_dweets = Dweet.objects.all().filter(reply_to=pk)
        serializer = self.get_serializer(remix_dweets, many=True)
        return Response(serializer.data)
