from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet)
# WARNING! Enabling this might cause unauthorized dweet posting
# router.register(r'dweets', views.DweetViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', RegistrationView.as_view(success_url='/')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^u/', include('dwitter.user.urls')),
    url(r'^dweet/', include('dwitter.dweet.urls')),
    url(r'^', include('dwitter.feed.urls')),
    url(r'^api/', include(router.urls)),
]
