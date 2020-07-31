from django.conf.urls import include, url
from dwitter.views import CommentViewSet, DweetViewSet, HashtagViewSet, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'comments', CommentViewSet)
router.register(r'dweets', DweetViewSet)
router.register(r'hashtags', HashtagViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]