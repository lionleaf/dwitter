from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',
        views.feed, {'page_nr': 1, 'sort': 'new'}, name='root'),

    url(r'^page/(?P<page_nr>\d+)$',
        views.feed, {'sort': 'new'}, name='feed_page'),

    url(r'^hot$',
        views.feed, {'page_nr': 1, 'sort': 'hot'}, name='hot_feed'),
    url(r'^hot/page/(?P<page_nr>\d+)$',
        views.feed, {'sort': 'hot'}, name='hot_feed_page'),

    url(r'^top$',
        views.feed, {'page_nr': 1, 'sort': 'top'}, name='top_feed'),
    url(r'^top/page/(?P<page_nr>\d+)$',
        views.feed, {'sort': 'top'}, name='top_feed_page'),

    url(r'^new$',
        views.feed, {'page_nr': 1, 'sort': 'new'}, name='new_feed'),
    url(r'^new/page/(?P<page_nr>\d+)$',
        views.feed, {'sort': 'new'}, name='new_feed_page'),

    url(r'^dweetreply/(?P<dweet_id>\d+)$',
        views.dweet_reply, name='dweet_reply'),

    url(r'^dweetdelete$',
        views.dweet_delete, name='dweet_delete'),

    url(r'^dweet$', views.dweet, name='dweet'),
    url(r'^like/(?P<post_id>\d+)$', views.like, name='like'),
]
