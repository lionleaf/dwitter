from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from dwitter.user.forms import UserSettingsForm


def user_settings(request, url_username):
    user = get_object_or_404(User, username=url_username)
    if request.user != user:
        return HttpResponse(status=403)

    if request.method == 'POST':
        user_settings_form = UserSettingsForm(request.POST, instance=user)
        if user_settings_form.is_valid():
            user = user_settings_form.save()
            messages.add_message(request, messages.INFO, 'Saved!')
        return redirect('user_settings', url_username=request.user.username)

    return render(request, 'user/settings.html', {
        'user': user,
        'settings_form': UserSettingsForm(instance=user)
    })
