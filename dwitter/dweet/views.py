from django.shortcuts import get_object_or_404, render
from dwitter.models import Dweet
from django.views.decorators.clickjacking import xframe_options_exempt


@xframe_options_exempt
def fullscreen_dweet(request, dweet_id):
    dweet = get_object_or_404(Dweet, id=dweet_id)

    context = {'code': dweet.code
               }
    return render(request, 'dweet/dweet.html', context)


@xframe_options_exempt
def blank_dweet(request):
    context = {'code': "c.width=1920;x.fillRect(800+S(t)*300,400,200,200)"
               }
    return render(request, 'dweet/dweet.html', context)
