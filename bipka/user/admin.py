from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib import messages
from django.template.loader import render_to_string
from .models import *
import requests
from django.contrib.sites.shortcuts import get_current_site
from .token import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect

class CustomUserAddForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'address_reg',
                  'address_fact', 'is_rest', 'is_ind_pred', 'is_superuser', 'password1', 'password2']
        labels = {
            'username': 'Полное имя организации',
            'email': 'Адрес электронной почты',
            'phone_no': 'Телефон',
            'head': 'Руководитель организации',
            'address_reg': 'Адрес регистрации',
            'address_fact': 'Фактический адрес',
            'ogrn': 'ОГРН/ОГРНИП',
            'inn': 'ИНН',
            'is_rest': 'Ресторан?',
            'is_ind_pred': 'ИП?',
            'is_superuser': 'Админ?'
        }
    def clean(self):
        cleaned_data = super().clean()  # Вызываем реализацию метода clean() родительского класса

        is_superuser = cleaned_data.get('is_superuser')
        is_ind_pred = cleaned_data.get('is_ind_pred')

        if not is_superuser:
            inn = cleaned_data.get('inn')
            ogrn = cleaned_data.get('ogrn')
            phone_no = cleaned_data.get('phone_no')

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

            if flag_check:
                return cleaned_data


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

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'address_reg',
                  'address_fact', 'is_rest', 'is_ind_pred', 'is_superuser', 'password', ]
        labels = {
            'username': 'Полное имя организации',
            'email': 'Адрес электронной почты',
            'phone_no': 'Телефон',
            'head': 'Руководитель организации',
            'address_reg': 'Адрес регистрации',
            'address_fact': 'Фактический адрес',
            'ogrn': 'ОГРН/ОГРНИП',
            'inn': 'ИНН',
            'is_rest': 'Ресторан?',
            'is_ind_pred': 'ИП?',
            'is_superuser': 'Админ?'
        }

@admin.register(CustomUser)
class MyUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserAddForm
    list_filter = ()
    list_display = ('email', 'phone_no', 'inn', 'ogrn', 'is_superuser', 'is_active')
    filter_horizontal = ()
    fieldsets = (
        (_('Изменить пароль'), {'fields': ('password', )}),
        (_('Personal info'), {'fields': ('username', 'phone_no', 'head', 'address_reg', 'address_fact', 'is_rest',
                                         'is_ind_pred', 'is_superuser')}),
    )
    add_fieldsets = (
        (_('Данные авторизации'), {'fields': ('email', 'password1', 'password2',)}),
        (_('Personal info'), {'fields': ('username', 'ogrn', 'inn', 'phone_no', 'head', 'address_reg', 'address_fact',
                                         'is_rest', 'is_ind_pred', 'is_superuser',)}),
    )
    def save_model(self, request, obj, form, change):
        if not change:
            # Если добавляем пользователя
            if not obj.is_superuser:
                obj.save()

                # Составляем письмо с ссылкой для подтверждения регистрации
                current_site = get_current_site(request)
                mail_subject = 'Подтверждение регистрации'
                message = render_to_string('acc_active_email.html', {
                    'user': obj.email,
                    'domain': current_site.domain,
                    'uid': obj.id,
                    'token': account_activation_token.make_token(obj),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                try:
                    email.send()
                except:
                    messages.error(request, 'Ошибка! Данная почта не существует.')
                    return super().save_model(request, obj, form, change)
            else:
                obj.is_staff = True
                obj.is_active = True
                obj.save()
        else:
            if obj.is_superuser:
                obj.is_staff = True
                obj.is_active = True
            else:
                obj.is_staff = False
            obj.save()
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        # Возвращает True, чтобы разрешить удаление экземпляра модели
        return True

    def delete_model(self, request, obj):
        # Действия по удалению экземпляра модели
        return super().delete_model(request, obj)

admin.site.register(Restaurant)
admin.site.register(Fund)
admin.site.register(Help)

@admin.register(OtpModel)
class OtpModelAdmin(admin.ModelAdmin):
    list_display = ("created_at", "is_active", "otp", "user", "id")[::-1]
