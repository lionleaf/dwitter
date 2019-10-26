from django.shortcuts import render


def about(request):
    return render(request, 'about.html', {'show_submit_box': True})
