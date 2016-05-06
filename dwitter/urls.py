"""dwitter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from . import views

urlpatterns = [
    url(r'^comment/(?P<dwwet_id>\d+)$', views.comment, name='comment'),

    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', RegistrationView.as_view(success_url='/')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^u/', include('dwitter.user.urls')),
    url(r'^dweet/', include('dwitter.dweet.urls')),
    url(r'^', include('dwitter.feed.urls')),
]
