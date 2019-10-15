from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views
from ..feed.views import NewUserFeed, HotUserFeed, TopUserFeed, NewLikedFeed

api_old = DefaultRouter()
api_old.register(r'comments', views.CommentViewSet)
api_old.register(r'dweets', views.DweetViewSet)
api_old.register(r'users', views.UserViewSet)

api_v1 = DefaultRouter()

urlpatterns = [
  path('', include(api_old.urls)),
  url(r'^v1/', include(api_v1.urls)),
]
