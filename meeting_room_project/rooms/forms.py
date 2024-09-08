from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField
from django.contrib.auth.models import User
from .models import Room

class CustomUserCreationForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()

class AddUserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label='Выберите пользователя')
