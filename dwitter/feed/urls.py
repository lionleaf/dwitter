from django.conf.urls import url
from . import views
from .views import HotDweetFeed, NewDweetFeed, RandomDweetFeed
from .views import TopWeekDweetFeed, TopMonthDweetFeed, TopYearDweetFeed, TopAllDweetFeed
from .views import NewHashtagFeed, TopHashtagFeed

urlpatterns = [
    url(r'^test/', HotDweetFeed.as_view()),

    url(r'^$', HotDweetFeed.as_view(), name='root'),
    url(r'^hot$', HotDweetFeed.as_view(), name='hot_feed'),

    # Default top to top of the month
    url(r'^top$', TopMonthDweetFeed.as_view(), name='top_feed'),
    url(r'^top/week$', TopWeekDweetFeed.as_view(), name='top_feed_week'),
    url(r'^top/month$', TopMonthDweetFeed.as_view(), name='top_feed_month'),
    url(r'^top/year$', TopYearDweetFeed.as_view(), name='top_feed_year'),
    url(r'^top/all$', TopAllDweetFeed.as_view(), name='top_feed_all'),

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
    url(r'^d/(?P<dweet_id>\d+)/report$', views.report_dweet, name='report_dweet'),
    url(r'^c/(?P<comment_id>\d+)/report$', views.report_comment, name='report_comment'),

    url(r'^e/(?P<dweet_id>\d+)$',
        views.dweet_embed, name='dweet_embed'),


    url(r'^dweet$', views.dweet, name='dweet'),
]
