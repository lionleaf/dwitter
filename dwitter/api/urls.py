from django.urls import include, path
#from django.conf.urls import url, include
from . import views
from ..feed.views import NewUserFeed, HotUserFeed, TopUserFeed, NewLikedFeed

urlpatterns = [
    path('', views.IndexView),
    
    path('dweets/', views.v0_DweetsView),
    path('dweets/<dweetId>', views.v0_DweetView),
    
    path('v1/', views.v1_IndexView),
    
  #url(r'^', include(api_old.urls)),
  #url(r'^v1/', include(api_v1.urls)),
]