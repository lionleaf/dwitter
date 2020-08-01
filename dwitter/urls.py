from django.conf.urls import include, url
from django.contrib import admin
from django.http import JsonResponse
from dwitter import urls_auth_v1
from dwitter import urls_dwitter_v1
from rest_framework import status
from rest_framework.decorators import api_view


@api_view()
def home(request):
    return JsonResponse(
        {'meta': {'copyright': 'Dwitter'}}
    )


@api_view()
def handler404(request, exception):
    return JsonResponse(
        {'errors': [{'status': '404', 'title': 'Not Found'}]},
        status=status.HTTP_400_BAD_REQUEST
    )


urlpatterns = [
    url(r'^$', home),
    url(r'^auth/v1/', include(urls_auth_v1)),
    url(r'^dwitter/v1/', include(urls_dwitter_v1)),
    url(r'^admin/', admin.site.urls),
]
