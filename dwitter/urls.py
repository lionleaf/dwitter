from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet)
# WARNING! Enabling this might cause unauthorized dweet posting
# router.register(r'dweets', views.DweetViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/register/$', RegistrationView.as_view(success_url='/')),
    url(r'^password/change/',
        auth_views.password_change,
        name='password_change'),
    url(r'^password/change/done/',
        auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^accounts/password/reset/confirm', auth_views.password_change),
    url(r'^u/', include('dwitter.user.urls')),
    url(r'^dweet/', include('dwitter.dweet.urls')),
    url(r'^', include('dwitter.feed.urls')),
    url(r'^api/', include(router.urls)),
]
