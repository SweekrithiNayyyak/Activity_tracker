# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    pass

class ActivityForm(forms.Form):
    study_hours = forms.FloatField(label='Hours spent to study')
    play_hours = forms.FloatField(label='Hours to play')
    sleep_hours = forms.FloatField(label='Hours to sleep')
    tv_hours = forms.FloatField(label='Hours to watch TV')