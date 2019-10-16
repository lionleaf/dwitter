from django.conf.urls import url, include
from . import views
from ..feed.views import NewUserFeed, HotUserFeed, TopUserFeed, NewLikedFeed

urlpatterns = [
  #path('', include(api_old.urls)),
  #url(r'^', include(api_old.urls)),
  #url(r'^v1/', include(api_v1.urls)),
]