from django.shortcuts import get_object_or_404, render
from dwitter.models import Dweet
from django.views.decorators.clickjacking import xframe_options_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page


def handler404(request):
    response = render_to_response('404_dweet.html', {},
                                  context_instance=RequestContext(request))
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
