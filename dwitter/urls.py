from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from dwitter import urls_accounts
from rest_framework import routers

'''
from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from django.contrib.auth import views as auth_views
from . import views
from . import views_v2
from rest_framework.routers import DefaultRouter
from django.conf import settings
from rest_framework.authtoken import views as authtoken_views
'''


router = routers.DefaultRouter(trailing_slash=False)

#router.register(r'accounts',include(urls_accounts))
#router.register(r'auth',class A{})
#router.register(r'dwitter', views.UserViewSet)

urlpatterns = [
    url(r'^',include(router.urls)),
    url(r'^admin/',admin.site.urls),
]
