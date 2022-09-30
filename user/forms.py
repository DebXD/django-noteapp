import email
from logging import PlaceHolder
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta():
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    EmailOrUsername = forms.CharField(label='Username or email address')
    password = forms.CharField(widget=forms.PasswordInput)
    remember = forms.BooleanField(required=False)

    class Meta():
        model = User
        fields = ['EmailOrUsername','password', 'remember']

class AccountUpdateForm(forms.ModelForm):# using ModelForm because we are fetching from user model
    username = forms.CharField(max_length=20, label='Your Username')
    email = forms.EmailField(label='Your Email')
    class Meta():
        model = User
        fields = ['username', 'email']