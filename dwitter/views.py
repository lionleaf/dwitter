from django.shortcuts import render
from dwitter.models import Comment
from dwitter.permissions import IsAuthorOrReadOnly
from dwitter.serializers import CommentSerializer
from django.utils import timezone
from rest_framework import viewsets, permissions


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fields = ('reply_to', 'author')
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, posted=timezone.now())

def about(request):
    return render(request, 'about.html')
