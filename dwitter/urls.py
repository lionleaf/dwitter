from django.conf.urls import url, include
from django.contrib import admin
from registration.backends.simple.views import RegistrationView
from django.contrib.auth import views as auth_views
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet)
router.register(r'dweets', views.DweetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/register/$',
        RegistrationView.as_view(success_url='/'),
        name='register'),
    url(r'^password/change/$',
        auth_views.PasswordChangeView.as_view(),
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.PasswordChangeDoneView.as_view(),
        name='password_change_done'),
    url(r'^password/reset/$',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    url(r'^password/reset/done/$',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^password/reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^about$',
        views.about,
        name='about'),


    url(r'^accounts/password/reset/confirm', auth_views.PasswordChangeView.as_view()),
    url(r'^u/', include('dwitter.user.urls')),
    url(r'^', include('dwitter.feed.urls')),
    url(r'^api/', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
