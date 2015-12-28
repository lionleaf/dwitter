from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^$', views.feed, name='feed'),
        url(r'^dweet', views.dweet, name='dweet'),
]
