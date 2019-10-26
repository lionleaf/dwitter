from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView),

    path('dweets/', views.v0_DweetsView),
    path('dweets/<dweetId>', views.v0_DweetView),

    path('v1/', views.v1_IndexView),
]
