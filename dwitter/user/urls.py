from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<url_username>[\w.@+-]+)$',
        views.user_feed, {'page_nr': '1', 'sort': 'new'}, name='user_feed'),
    url(r'^(?P<url_username>[\w.@+-]+)/(?P<sort>hot|new|top|old)$',
        views.user_feed, {'page_nr': '1'}, name='user_sort_feed'),
    url(r'^(?P<url_username>[\w.@+-]+)/'
        '(?P<sort>hot|new|top|old)/(?P<page_nr>\d+)$',
        views.user_feed, name='user_feed_page'),
    url(r'^(?P<url_username>[\w.@+-]+)/awesome$',
        views.user_liked, {'page_nr': '1', 'sort': 'new'}, name='user_liked'),
    url(r'^(?P<url_username>[\w.@+-]+)/awesome/(?P<sort>hot|new|top|old)$',
        views.user_liked, {'page_nr': '1'}, name='user_sort_liked'),
    url(r'^(?P<url_username>[\w.@+-]+)/'
        '(?P<sort>hot|new|top|old)/awesome/(?P<page_nr>\d+)$',
        views.user_liked, name='user_liked_page'),
    url(r'^(?P<url_username>[\w.@+-]+)/settings$',
        views.user_settings, name='user_settings'),
    ]
