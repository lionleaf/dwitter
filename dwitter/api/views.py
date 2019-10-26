from django.http import JsonResponse
from dwitter.templatetags.to_gravatar_url import to_gravatar_url
# from .models import //Comment, Dweet
# from .models import APIDweet
from ..models import Dweet


def IndexView(request):
    json = {
        "comments": "https://www.dwitter.net/api/comments/",
        "dweets": "https://www.dwitter.net/api/dweets/",
    }

    return JsonResponse(json, safe=False)


def v0_DweetView(request, dweetId):
    dweetId = int(dweetId)
    try:
        dweet = Dweet.objects.get(pk=dweetId)

        json = {
            "id": dweet.id,
            "code": dweet.code,
            "posted": dweet.posted,
            "author": {
                "username": dweet.author.username,
                "date_joined": dweet.author.date_joined,
                "link": "https://www.dwitter.net/u/%s" % dweet.author.username,
                "avatar": to_gravatar_url(dweet.author.email),
            },
            # "link": dweet.link,
            # "awesome_count": dweet.likes,
            "remix_of": dweet.reply_to.id if dweet.reply_to is not None else None,
        }
    except Exception:
        json = {
            "detail": "Not found.",
        }

    return JsonResponse(json, safe=False)


def v0_DweetsView(request):
    dweets = Dweet.objects.all()

    limit = int(request.GET.get('limit', 10))
    if limit < 1:
        limit = 10

    offset = int(request.GET.get('offset', 0))
    if offset < 0:
        offset = 0

    page = (offset-(offset % limit))/limit
    lastpage = len(dweets) % limit
    if page > lastpage:
        page = lastpage

    results = []

    for dweet in dweets[offset:(limit + offset if limit is not None else None)]:
        d = {
            "id": dweet.id,
            "code": dweet.code,
            "posted": dweet.posted,
            "author": {
                "username": dweet.author.username,
                "date_joined": dweet.author.date_joined,
                "link": "https://www.dwitter.net/u/%s" % dweet.author.username,
                "avatar": to_gravatar_url(dweet.author.email),
            },
            # "link": dweet.link,
            # "awesome_count": dweet.likes,
            "remix_of": dweet.reply_to.id if dweet.reply_to is not None else None,
        }
        results.append(d)

    url_limit = "https://www.dwitter.net/api/dweets/?limit="+str(limit)

    url_prev = url_limit+"&offset="+str(offset+limit)
    url_next = url_limit+("&offset="+str(offset-limit) if offset-limit > 0 else "")

    json = {
        "_": page,
        "_2": lastpage,
        "count": len(results),
        "next": None if (page > lastpage) else url_prev,
        "previous": None if (page == 0) else url_next,
        "results": results,
    }

    return JsonResponse(json, safe=False)


def v1_IndexView(request):
    json = {
        "errors": [
            {
                "status": "404",
                "title": "Not Found",
                "detail": "The endpoint could not be found",
            }
        ]
    }

    return JsonResponse(json, safe=False)


# class TestViewSet():
    # return 0
    # queryset = Dweet.objects.all()


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
