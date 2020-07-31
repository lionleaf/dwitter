import traceback
from django.conf.urls import include, url
from django.contrib import admin
from dwitter import urls_auth_v1
from dwitter import urls_dwitter_v1
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view()
def home(request):
    return Response({'meta':{'copyright':'Dwitter'}})
    
@api_view()
def handler404(request,exception):
    tb = traceback.format_exc()
    return Response({'errors':[{'status':'404','title':'Not Found'}]})

urlpatterns = [
    url(r'^$',home),
    url(r'^auth/v1/',include(urls_auth_v1)),
    url(r'^dwitter/v1/',include(urls_dwitter_v1)),
    url(r'^admin/',admin.site.urls),
]
