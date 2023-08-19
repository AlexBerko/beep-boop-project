from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
import requests
#from validate_email_address import validate_email

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
    def clean(self):
        cleaned_data = super().clean()  # Вызываем реализацию метода clean() родительского класса

        inn = cleaned_data.get('inn')
        ogrn = cleaned_data.get('ogrn')
        phone_no = cleaned_data.get('phone_no')
        email = cleaned_data.get('email')

        flag_check = False
        if not inn or not ogrn:
            return cleaned_data

        if not inn.isdigit():
            self.add_error('inn',
                           'Ошибка! ИНН должно быть числом.')
            flag_check = True
        if not ogrn.isdigit():
            self.add_error('ogrn',
                           'Ошибка! ОГРН/ОГРНИП должно быть числом.')
            flag_check = True

        if phone_no:
            if not phone_no.isdigit():
                self.add_error('phone_no',
                               'Ошибка! Номер телефона начинается с 8, далее идут цифры без тире и пробелов.')
                flag_check = True
        '''
        if email:
            if not validate_email(email, verify=True):
                self.add_error('email',
                               'Ошибка! Указанная почта не существует!')
                flag_check = True
        '''

        if flag_check:
            return cleaned_data

        is_ind_pred = cleaned_data.get('is_ind_pred')
        api_key = 'CAYR4QAsioUmKS5o'
        site = 'company'
        if is_ind_pred:
            site = 'entrepreneur'

        is_org_found = False

        response = requests.get(
            'https://api.checko.ru/v2/' + site + '?key=' + api_key + '&inn=' + inn + '&source=true')
        # если запрос завершился успешно
        if response.status_code == 200:
            data = response.json()
            # если отсутствует сообщение об ошибке
            if 'message' not in data['meta']:
                is_org_found = True

        if not is_org_found:
            response = requests.get(
                'https://api.checko.ru/v2/' + site + '?key=' + api_key + '&ogrn=' + ogrn + '&source=true')
            if response.status_code == 200:
                data = response.json()
                # если есть сообщение об ошибке
                if 'message' in data['meta']:
                    self.add_error('inn', 'Не удалось найти организацию с указанными данными! Пропробуйте изменить'
                                          ' тип организации (вместо ИП сделать юр. лицо и наоборот).')
                    self.add_error('ogrn', 'Не удалось найти организацию с указанными данными! Пропробуйте изменить'
                                          ' тип организации (вместо ИП сделать юр. лицо и наоборот).')
                    return cleaned_data
            else:
                self.add_error('inn',
                               'API-вызов завершился неудачей. Попробуйте изменить данные ИНН/ОГРН и попробуйте позже.')
                return cleaned_data

        data = response.json()
        info = data['data']

        if cleaned_data.get('is_ind_pred'):
            api_ogrn = info['ОГРНИП']
        else:
            api_ogrn = info['ОГРН']
        api_inn = info['ИНН']

        if api_inn != inn or api_ogrn != ogrn:
            self.add_error('inn',
                           'Ошибка! Не удалось найти организацию с текущей комбинацией ИНН и ОГРН.')
            self.add_error('ogrn',
                           'Ошибка! Не удалось найти организацию с текущей комбинацией ИНН и ОГРН.')
            return cleaned_data

        return cleaned_data
