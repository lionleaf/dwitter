#from django.urls import include, path
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from registration.backends.simple.views import RegistrationView

from . import api
from . import views

urlpatterns = [
    url(r'^', include('dwitter.feed.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('dwitter.api.urls')),
    url(r'^u/', include('dwitter.user.urls')),

    url(r'^accounts/register/$',
        RegistrationView.as_view(success_url='/'),
        name='register'),
    url(r'^password/change/$',
        auth_views.password_change,
        name='password_change'),
    url(r'^password/change/done/$',
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
    url(r'^about$',
        views.about,
        name='about'),


    url(r'^accounts/password/reset/confirm', auth_views.password_change),
    
    
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns