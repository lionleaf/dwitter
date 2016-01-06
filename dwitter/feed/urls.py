from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.feed, name='feed'),
        url(r'^dweet', views.dweet, name='dweet'),
        url(r'^like/(?P<post_id>[0-9]*)', views.like, name='like'),
]
