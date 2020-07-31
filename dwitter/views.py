from dwitter.models import Comment, Dweet, Hashtag, User
from dwitter.serializers import CommentSerializer, DweetSerializer, HashtagSerializer, UserSerializer
from rest_framework_json_api.pagination import JsonApiPageNumberPagination

from rest_framework_json_api.views import ModelViewSet, RelationshipView

class CommentViewSet(ModelViewSet):
    pagination_class = JsonApiPageNumberPagination
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
class DweetViewSet(ModelViewSet):
    pagination_class = JsonApiPageNumberPagination
    queryset = Dweet.objects.all()
    serializer_class = DweetSerializer
    
class HashtagViewSet(ModelViewSet):
    pagination_class = JsonApiPageNumberPagination
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    #multiple_lookup_fields = ['pk','name']
    
class UserViewSet(ModelViewSet):
    pagination_class = JsonApiPageNumberPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #multiple_lookup_fields = ['pk','username']