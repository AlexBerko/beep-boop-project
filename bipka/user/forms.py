from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


# class LoginForm(forms.Form):
#     email = forms.CharField(max_length=65)
#     password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'address_reg',
                  'address_fact', 'is_rest', 'password1', 'password2']
        labels = {
            'username': 'Полное имя организации',
            'email': 'Адрес электронной почты',
            'phone_no': 'Телефон',
            'head': 'Руководитель организации',
            'address_reg': 'Адрес регистрации',
            'address_fact': 'Фактический адрес',
            'ogrn': 'ОГРН/ОГРНИП',
            'inn': 'ИНН',
            'is_rest': 'Ресторан?'
        }

class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = ['title', 'full_info']
        # model.org_info
