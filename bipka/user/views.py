import math
import random

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import re

from bipka import settings

from django.contrib.auth import authenticate, login, get_user_model, logout
from django.template.loader import render_to_string

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .forms import *
from .serializers import *
from .token import account_activation_token
from main.views import get_user_from_header
import secrets
import datetime
from rest_framework.authtoken.models import Token
from datetime import timedelta

#################################################
#                                               #
#                   OTP  VIEWS                  #
#                                               #
#################################################

# for alpha numeric OTP
def otp_provider():
    corpus = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    generate_OTP = ""
    size = 7
    length = len(corpus)
    for i in range(size):
        generate_OTP += corpus[math.floor(random.random() * length)]
    return generate_OTP


def send_email_with_html(recipient_email, subject, template_name, context):
    msg = MIMEMultipart()
    html_message = render_to_string(template_name, context)
    mime_text = MIMEText(html_message, 'html')
    msg.attach(mime_text)

    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = recipient_email
    msg['Subject'] = subject

    try:
        smtp_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        smtp_server.starttls()
        smtp_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp_server.send_message(msg)
        smtp_server.quit()
        return True
    except Exception as e:
        return False


def send_otp_in_mail(user, otp):
    subject = 'Код подтверждения аутентификации'
    # message = f'Здравствуйте, {user.email}!\n Для завершения аутентификации введите следующий код: {otp.otp}'
    email_from = settings.EMAIL_HOST_USER
    # recipient_list = [user.email, ]
    # send_mail(subject, message, email_from, recipient_list)
    context = {'user': user.email,
               'otp': otp.otp
               }

    return send_email_with_html(user.email, subject, 'otp_email.html', context)


class OtpCheck_API(APIView):
    def post(self, request):
        if 'hash' not in request.data:
            return Response({'error': 'Hash не указан.'}, status=400)
        if 'code' not in request.data:
            return Response({'error': 'Код не указан.'}, status=400)
        get_hash = request.data.get('hash')
        get_code = request.data.get('code')

        try:
            verify_otp = OtpModel.objects.get(hash=get_hash)
        except:
            return Response({'error': 'Неверный хэш.'}, status=400)
        if not verify_otp.otp == get_code:
            return Response({'error': 'Неверный код.'}, status=400)

        user = CustomUser.objects.get(id=verify_otp.user_id)

        token, created = Token.objects.get_or_create(user=user)
        if not created and (timezone.now() - token.created) > timedelta(days=1):
            token.delete()
            token = Token.objects.create(user=user)

        # Возврат токена
        return Response({'auth_token': token.key})



#################################################
#                                               #
#                   USER VIEWS                  #
#                                               #
#################################################


#### API-регистрация ######
class SignUP(APIView):
    def post(self, request):
        form = RegisterForm(request.data)
        if form.is_valid():
            user = form.save(commit=False)

            ###################################################
            #                   ДОП ЗАДАНИЕ                   #
            ###################################################

            # Проверка, что такая организация существует с помощью стороннего API
            inn = user.inn
            ogrn = user.ogrn
            site = 'company'
            if user.is_ind_pred:
                site = 'entrepreneur'

            is_org_found = False

            response = requests.get(
                'https://api.checko.ru/v2/' + site + '?key=' + settings.API_KEY + '&inn=' + inn + '&source=true')
            # если запрос завершился успешно
            if response.status_code == 200:
                data = response.json()
                # если отсутствует сообщение об ошибке
                if 'message' not in data['meta']:
                    is_org_found = True

            if not is_org_found:
                response = requests.get(
                    'https://api.checko.ru/v2/' + site + '?key=' + settings.API_KEY + '&ogrn=' + ogrn + '&source=true')
                if response.status_code == 200:
                    data = response.json()
                    # если есть сообщение об ошибке
                    if 'message' in data['meta']:
                        return Response({'error': 'Не удалось найти организацию с указанными данными!'}, status=400)
                else:
                    return Response({'error': 'Ошибка запроса при поиске организации!'}, status=400)

            data = response.json()
            info = data['data']

            if user.is_ind_pred:
                api_ogrn = info['ОГРНИП']
            else:
                api_ogrn = info['ОГРН']
            api_inn = info['ИНН']

            if api_inn != inn or api_ogrn != ogrn:
                return Response({'error': 'Ошибка! Не удалось найти организацию с текущей комбинацией ИНН и ОГРН.'},
                                status=400)

            if user.is_ind_pred:
                fio = info['ФИО']
                if fio != user.head:
                    return Response({'error': 'Ошибка! Неверное имя владельца ИП.'}, status=400)
                pattern = r'^ИП\s+[А-Яа-я]+\s+[А-Яа-я]+\s*[А-Яа-я]*$'
                if not re.match(pattern, user.username):
                    return Response({'error': 'Ошибка! Неверный формат имени ИП.'}, status=400)
                str_name = user.username
                str_name_split = str_name.split('ИП', 1)[-1].strip()
                if not str_name_split == user.head:
                    return Response({'error': 'Ошибка! Указанное имя ИП и владелец не совпадают.'}, status=400)

            else:
                ruk_array = info['Руковод']
                is_fio_found = False
                for fio in ruk_array:
                    if fio['ФИО'] == user.head:
                        is_fio_found = True
                        break
                if not is_fio_found:
                    return Response({'error': 'Ошибка! Указанный пользователь не был найден в списке руководителей'
                                              ' организации'}, status=400)

                #if user.username != info['НаимПолн']:
                #    return Response({'error': 'Ошибка в наименовании организации (необходимо указать полное имя).'},
                #                    status=400)

            # SQL-инъекция
            #conn = sqlite3.connect('db.sqlite3')
            #cursor = conn.cursor()

            #username = user.username
            #password = user.password
            #email = user.email
            #phone_no = user.phone_no
            #head = user.head
            #address_reg = user.address_reg
            #address_fact = user.address_fact
            #is_rest = user.is_rest
            #is_ind_pred = user.is_ind_pred
            #date_reg = datetime.datetime.now()
            #cursor.executescript(
            #    '''INSERT INTO user_customuser (username, password, email, phone_no, head, ogrn, inn, is_rest, is_ind_pred, date_reg, is_active, is_staff, is_superuser, address_reg, address_fact) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, {}, '{}', FALSE, FALSE, FALSE, '{}', '{}')'''
            #    .format(username, password, email, phone_no, head, ogrn, inn, is_rest, is_ind_pred, date_reg,
            #            address_reg, address_fact))

            #conn.commit()
            #conn.close()

            # Составляем письмо с ссылкой для подтверждения регистрации
            mail_subject = 'Подтверждение регистрации'
            to_email = form.cleaned_data.get('email')

            context = {
                'user': user.email,
                'uid': user.id,
                'token': account_activation_token.make_token(user),
            }

            if not send_email_with_html(to_email, mail_subject, 'acc_active_email.html', context):
                return Response({'error': 'Ошибка отправки сообщения на почту.'}, status=400)

            # После проверки и отправки письма сохраняем пользователя в БД
            user.save()

            serializer = UserRegSerializer(user)
            json = JSONRenderer().render(serializer.data)
            return Response(json, status=200)
        else:
            return Response(form.errors, status=400)


#### API-подтверждение почты ######
class ActivateAccount_API(APIView):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            user = CustomUser.objects.get(id=uidb64)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(status=200)
        else:
            return Response(status=400)


#### API-профиля ######
@permission_classes([IsAuthenticated])
class OrgDetailView(APIView):
    def get(self, request):
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)
        serializer = OrgDetailSerializer(current_user)
        json = JSONRenderer().render(serializer.data)
        return Response(json, status=200)

    def put(self, request):
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)

        if 'phone_no' in request.data:
            current_user.phone_no = request.data['phone_no']
        if 'address_reg' in request.data:
            current_user.address_reg = request.data['address_reg']
        if 'address_fact' in request.data:
            current_user.address_fact = request.data['address_fact']
        current_user.save()
        return Response(status=200)

    def post(self, request):
        user = get_user_from_header(request)
        if not user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)

        if 'old_password' not in request.data:
            return Response({'error': 'Старый пароль не указан.'}, status=400)
        if 'new_password' not in request.data:
            return Response({'error': 'Новый пароль не указан.'}, status=400)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'status': 'Пароль успешно изменен.'}, status=200)
        else:
            return Response({'error': 'Неверный старый пароль.'}, status=400)

    def delete(self, request):
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)

        current_user.delete()
        return Response(status=200)



@permission_classes([IsAuthenticated])
class UserByID_API(APIView):
    def get(self, request, pk):
        try:
            current_user = CustomUser.objects.get(id=pk)
        except:
            return Response({'error': 'Пользователь с данным id не обнаружен.'}, status=400)

        serializer = OrgDetailSerializer(current_user)
        json = JSONRenderer().render(serializer.data)
        return Response(json, status=200)

class SignIN_API(APIView):
    def post(self, request):
        if 'email' not in request.data:
            return Response({'error': 'Почта не указана.'}, status=400)
        if 'password' not in request.data:
            return Response({'error': 'Пароль не указан.'}, status=400)

        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except:
            return Response({'error': 'Пользователя не существует.'}, status=400)

        if not user.is_active:
            return Response({'error': 'Сначала подтвердите почту.'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Неправильный пароль.'}, status=400)

        OtpModel.objects.filter(user=user).delete()
        hash_otp = secrets.token_hex(16)
        otp_stuff = OtpModel.objects.create(user=user, otp=otp_provider(), hash=hash_otp)
        if send_otp_in_mail(user, otp_stuff):
            return Response({'hash': hash_otp}, status=200)
        else:
            return Response({'error': 'Ошибка отправки кода на почту.'}, status=400)

@permission_classes([IsAuthenticated])
class ChangePassword_API(APIView):
    def post(self, request):
        if 'old_password' not in request.data:
            return Response({'error': 'Старый пароль не указан.'}, status=400)
        if 'new_password' not in request.data:
            return Response({'error': 'Новый пароль не указан.'}, status=400)

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        user = get_user_from_header(request)

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({'status': 'Пароль успешно изменен.'}, status=200)
        else:
            return Response({'error': 'Неверный старый пароль.'}, status=400)























class OtpVerifyView_API(APIView):
    def post(self, request):
        otp = request.data.get('otp')
        verify_otp = OtpModel.objects.filter(otp=otp)
        if verify_otp.exists():
            # login(request, verify_otp[0].user)
            return Response(status=200)
        else:
            return Response({'error': 'Ошибка! Неверный код'}, status=400)


class OTP_send(APIView):
    def post(self, request):
        if 'email' not in request.data:
            return Response({'error': 'Почта не указана.'}, status=400)
        if 'password' not in request.data:
            return Response({'error': 'Пароль не указан.'}, status=400)

        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователя не существует.'}, status=400)

        if not user.is_active:
            return Response({'error': 'Сначала подтвердите почту.'}, status=400)

        if not user.check_password(password):
            return Response({'error': 'Неправильный пароль.'}, status=400)

        OtpModel.objects.filter(user=user).delete()
        otp_stuff = OtpModel.objects.create(user=user, otp=otp_provider())
        if send_otp_in_mail(user, otp_stuff):
            return Response(status=200)
        else:
            return Response({'error': 'Ошибка отправки кода на почту.'}, status=400)

