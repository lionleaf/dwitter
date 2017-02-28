from django.contrib.auth import get_user_model
from django.forms import ModelForm


class UserSettingsForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)
