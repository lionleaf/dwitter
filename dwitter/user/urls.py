from django.conf.urls import url
from . import views
from ..feed.views import NewUserFeed, HotUserFeed, TopUserFeed, NewLikedFeed

urlpatterns = [
    url(r'^(?P<url_username>[\w.@+-]+)$', NewUserFeed.as_view(), name='user_feed'),
    url(r'^(?P<url_username>[\w.@+-]+)/hot$', HotUserFeed.as_view(), name='hot_user_feed'),
    url(r'^(?P<url_username>[\w.@+-]+)/top$', TopUserFeed.as_view(), name='top_user_feed'),

    url(r'^(?P<url_username>[\w.@+-]+)/awesome$', NewLikedFeed.as_view(), name='user_liked'),

    url(r'^(?P<url_username>[\w.@+-]+)/settings$', views.user_settings, name='user_settings'),
    ]
