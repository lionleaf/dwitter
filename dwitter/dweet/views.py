from django.shortcuts import get_object_or_404, render
from dwitter.models import Dweet
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.cache import cache_page


def handler404(request, *args, **kwargs):
    response = render(request, '404_dweet.html')
    response.status_code = 404
    return response


@xframe_options_exempt
@cache_page(3600)
def fullscreen_dweet(request, dweet_id):
    dweet = get_object_or_404(Dweet, id=dweet_id)

    context = {
        'code': dweet.code,
        'newDweet': 'false',
    }
    return render(request, 'dweet/dweet.html', context)


@xframe_options_exempt
@cache_page(3600)
def blank_dweet(request):
    context = {
        'code': "c.width=1920;x.fillRect(800+S(t)*300,400,200,200)",
        'newDweet': 'true',
    }
    return render(request, 'dweet/dweet.html', context)
