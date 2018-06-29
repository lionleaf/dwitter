from django.conf.urls import url
from . import views
from .views import HotDweetFeed, TopDweetFeed, NewDweetFeed, RandomDweetFeed
from .views import NewHashtagFeed, TopHashtagFeed

urlpatterns = [
    url(r'^test/', HotDweetFeed.as_view()),

    url(r'^$', HotDweetFeed.as_view(), name='root'),
    url(r'^hot$', HotDweetFeed.as_view(), name='hot_feed'),
    url(r'^top$', TopDweetFeed.as_view(), name='top_feed'),
    url(r'^new$', NewDweetFeed.as_view(), name='new_feed'),
    url(r'^random$', RandomDweetFeed.as_view(), name='random_feed'),

    url(r'^h/(?P<hashtag_name>[\w._]+)$', NewHashtagFeed.as_view(), name='hashtag_feed'),
    url(r'^h/(?P<hashtag_name>[\w._]+)/top$', TopHashtagFeed.as_view(), name='top_hashtag_feed'),

    url(r'^d/(?P<dweet_id>\d+)$',
        views.dweet_show, name='dweet_show'),
    url(r'^d/(?P<dweet_id>\d+)/reply$',
        views.dweet_reply, name='dweet_reply'),
    url(r'^d/(?P<dweet_id>\d+)/delete$',
        views.dweet_delete, name='dweet_delete'),
    url(r'^d/(?P<dweet_id>\d+)/like$', views.like, name='like'),

    url(r'^e/(?P<dweet_id>\d+)$',
        views.dweet_embed, name='dweet_embed'),


    url(r'^dweet$', views.dweet, name='dweet'),
]
