from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'^lionleaf$', views.lionleaf, name='lionleaf'),
]
