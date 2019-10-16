from django.conf.urls import url, include
from . import views
from .. import views as views_old
from ..feed.views import NewUserFeed, HotUserFeed, TopUserFeed, NewLikedFeed

urlpatterns = [
    url(r'/',HotUserFeed),
  #path('', include(api_old.urls)),
  #url(r'^', include(api_old.urls)),
  #url(r'^v1/', include(api_v1.urls)),
]