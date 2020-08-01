from django.conf.urls import include, url
from dwitter.views import CommentRelationshipView, CommentViewSet, DweetRelationshipView, DweetViewSet, HashtagRelationshipView, HashtagViewSet, UserRelationshipView, UserViewSet
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

router.register(r'comments', CommentViewSet)
router.register(r'dweets', DweetViewSet)
router.register(r'hashtags', HashtagViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    
    
    url(r'^comments/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)$',
        CommentRelationshipView.as_view(),
        name='blog-relationships'),
    url(r'^dweets/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)$',
        DweetRelationshipView.as_view(),
        name='blog-relationships'),
    url(r'^hashtags/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)$',
        HashtagRelationshipView.as_view(),
        name='blog-relationships'),
    url(r'^users/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)$',
        UserRelationshipView.as_view(),
        name='blog-relationships'),
]