from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.feed,{'page_nr' : 1}, name='feed'),
        url(r'^page/(?P<page_nr>\d+)$', views.feed, name='feed'),
        url(r'^dweet$', views.dweet, name='dweet'),
        url(r'^like/(?P<post_id>\d+)$', views.like, name='like'),
]
