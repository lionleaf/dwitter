from django.conf.urls import url
from . import views
from ..feed.views import NewUserFeed, HotUserFeed, TopUserFeed, NewLikedFeed

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet)
router.register(r'dweets', views.DweetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = router.urls
