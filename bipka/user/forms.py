from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    is_rest = forms.TypedChoiceField(
        choices=[(True, 'Ресторан'), (False, 'Благотворительная организация')],
        label='Тип организации:',
        required=False,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect
    )
    is_ind_pred = forms.TypedChoiceField(
        choices=[(True, 'ИП'), (False, 'Юридическое лицо')],
        label='Вид деятельности',
        required=False,
        coerce=lambda x: x == 'True',
        widget=forms.RadioSelect
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'address_reg',
                  'address_fact', 'is_rest', 'is_ind_pred', 'password1', 'password2']
        labels = {
            'username': 'Полное имя организации',
            'email': 'Адрес электронной почты',
            'phone_no': 'Телефон',
            'head': 'Руководитель организации',
            'address_reg': 'Адрес регистрации',
            'address_fact': 'Фактический адрес',
            'ogrn': 'ОГРН/ОГРНИП',
            'inn': 'ИНН'
        }

class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = ['title', 'full_info']
        # model.org_info
