from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


# class LoginForm(forms.Form):
#     email = forms.CharField(max_length=65)
#     password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'kpp', 'address_reg',
                  'address_fact', 'is_rest', 'is_blago', 'password1', 'password2']

