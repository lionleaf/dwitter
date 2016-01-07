from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^(?P<url_username>[a-z0-9]*)$', views.user_feed, {'page_nr':'1'}, name='user_feed'),
        url(r'^(?P<url_username>[a-z0-9]*)/(?P<page_nr>\d+)$', views.user_feed, name='user_feed_page'),
]
