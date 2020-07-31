from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from dwitter import urls_accounts
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def home(request):
    return Response({'meta':{'copyright':'Dwitter'}})
    
@api_view()
def handler404(request,exception):
    return Response({'errors':[{'status':'404','title':'Not Found'}]})

router = routers.DefaultRouter(trailing_slash=False)

#router.register(r'accounts',include(urls_accounts))
#router.register(r'auth',class A{})
#router.register(r'dwitter', views.UserViewSet)

urlpatterns = [
    url(r'^$',home),
    url(r'^',include(router.urls)),
    url(r'^admin/',admin.site.urls),
]
