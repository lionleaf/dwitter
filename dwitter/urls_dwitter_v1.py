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
        
    url(r'^comments/(?P<pk>[^/.]+)/(?P<related_field>\w+)$',
        CommentViewSet.as_view({'get': 'retrieve_related'}),
        name='comment-related'),
    url(r'^dweets/(?P<pk>[^/.]+)/(?P<related_field>\w+)$',
        DweetViewSet.as_view({'get': 'retrieve_related'}),
        name='dweet-related'),
    url(r'^hashtags/(?P<pk>[^/.]+)/(?P<related_field>\w+)$',
        HashtagViewSet.as_view({'get': 'retrieve_related'}),
        name='hashtag-related'),
    url(r'^users/(?P<pk>[^/.]+)/(?P<related_field>\w+)$',
        UserViewSet.as_view({'get': 'retrieve_related'}),
        name='user-related'),
    
    
    url(r'^comments/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)$',
        CommentRelationshipView.as_view(),
        name='comment-relationships'),
    url(r'^dweets/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)$',
        DweetRelationshipView.as_view(),
        name='dweet-relationships'),
    url(r'^hashtags/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)$',
        HashtagRelationshipView.as_view(),
        name='hashtag-relationships'),
    url(r'^users/(?P<pk>[^/.]+)/relationships/(?P<related_field>\w+)$',
        UserRelationshipView.as_view(),
        name='user-relationships'),
]