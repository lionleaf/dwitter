#from .models import //Comment, Dweet
#from .models import APIDweet
from ..models import Dweet

class TestViewSet():
    queryset = Dweet.objects.all()
    
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


class DweetFilterSet(FilterSet):
    remix_of = NumberFilter(name='reply_to')
    author = CharFilter(name='author__username')

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

'''