import math
import random

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
import re

from bipka import settings

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth import get_user

from .forms import *
from .serializers import *
from .token import account_activation_token
from main.views import get_user_from_header


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


# Otp email sender
def send_otp_in_mail(user, otp):
    subject = 'Код подтверждения аутентификации'
    message = f'Здравствуйте, {user.email}!\n Для завершения аутентификации введите следующий код: {otp.otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(subject, message, email_from, recipient_list)


class OtpVerifyView_API(APIView):
    def get(self, request):
        return Response(status=200)

    def post(self, request):
        otp = request.data.get('otp')
        verify_otp = OtpModel.objects.filter(otp=otp)
        if verify_otp.exists():
            #login(request, verify_otp[0].user)
            return Response(status=200)
        else:
            return Response({'error': 'Ошибка! Неверный код'}, status=400)


#################################################
#                                               #
#                   USER VIEWS                  #
#                                               #
#################################################


#### API-регистрация ######
class SignUP(APIView):
    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)

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
                    return Response({'error': 'Ошибка! Указанное имя ИП и владелей не совпадают.'}, status=400)

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

                if user.username != info['НаимПолн']:
                    return Response({'error': 'Ошибка в наименовании организации (необходимо указать полное имя).'},
                                    status=400)


            # После проверки сохраняем пользователя в БД
            user.save()

            # Составляем письмо с ссылкой для подтверждения регистрации
            current_site = get_current_site(request)
            mail_subject = 'Подтверждение регистрации'
            message = render_to_string('acc_active_email.html', {
                'user': user.email,
                'domain': current_site.domain,
                'uid': user.id,
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            try:
                email.send()
            except:
                return Response({'error': 'Ошибка отправки сообщения на почту.'}, status=400)

            serializer = UserRegSerializer(user)
            json = JSONRenderer().render(serializer.data)
            return Response(json, status=200)
            # messages.info(request,
            #              'Данные успешно сохранены! Для завершения регистрации подтвердите адрес электронной почты.')
            # return redirect('/signin/')
        else:
            return Response(form.errors, status=400)


#### API-подтверждение почты ######
class ActivateAccount_API(APIView):
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            user = User.objects.get(id=uidb64)
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

    def post(self, request):
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)

        if 'new_password' not in request.data:
            return Response({'error': 'Новый пароль не получен.'}, status=400)

        new_pwd = request.data.get('new_password')
        current_user.password = make_password(new_pwd)
        current_user.save()
        return Response(status=200)

    '''
    def delete(self, request):
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)

        current_user.delete()
        return Response(status=200)
    '''



class OTP_send(APIView):
    def post(self, request):
        if 'email' not in request.data:
            return Response({'error': 'Почта не указана.'}, status=400)

        email = request.data.get('email')
        try:
            user = CustomUser.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Пользователя не существует.'}, status=400)

        if not user.is_active:
            return Response({'error': 'Сначала подтвердите почту.'}, status=400)

        OtpModel.objects.filter(user=user).delete()
        otp_stuff = OtpModel.objects.create(user=user, otp=otp_provider())
        send_otp_in_mail(user, otp_stuff)
        return Response(status=200)













#################################################
#                                               #
#              СТАРЫЕ НАРАБОТКИ                 #
#                                               #
#################################################


#### API-авторизация ######
class SignIN(APIView):
    def get(self, request):
        return Response(status=200)

    def post(self, request):
        email = request.data.get('email')
        pwd = request.data.get('password')
        if 'email' not in request.data or 'password' not in request.data:
            return Response({'error': 'Ошибка! Пропущен пароль и/или почта.'}, status=400)

        if (email == "") or (pwd == ""):
            return Response({'error': 'Ошибка! Пропущен пароль или почта.'}, status=400)

        user = authenticate(email=email, password=pwd)
        if user is None:
            return Response({'error': 'Ошибка! Пользователь с указанными учетными данными не найден.'}, status=400)
        else:
            if user.is_superuser:
                login(request, user)
                return Response({'message': 'Суперпользователь.'}, status=200)
                # return redirect('/').
            else:
                if not user.is_active:
                    return Response({'error': 'Ошибка! Почта не подтверждена.'}, status=400)
                OtpModel.objects.filter(user=user).delete()
                otp_stuff = OtpModel.objects.create(user=user, otp=otp_provider())
                send_otp_in_mail(user, otp_stuff)
                return Response(status=200)




class LogOUT_API(APIView):
    def get(self, request):
        logout(request)
        return Response(status=200)




# @api_view(['POST', 'GET'])
def sign_up(request):
    if request.method == 'GET':  # выводит форму
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            # Составляем письмо с ссылкой для подтверждения регистрации
            current_site = get_current_site(request)
            mail_subject = 'Подтверждение регистрации'
            message = render_to_string('acc_active_email.html', {
                'user': user.email,
                'domain': current_site.domain,
                'uid': user.id,
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            try:
                email.send()
            except:
                error_message = 'Ошибка! Указанная почта не существует.'
                return render(request, 'register.html', {'form': form, 'error_message': error_message})

            messages.info(request,
                          'Данные успешно сохранены! Для завершения регистрации подтвердите адрес электронной почты.')
            return redirect('/signin/')

            '''
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            json_object = json.loads(request.body)
            data_raw = JSONParser().parse(json_object)  # data after parsing
            serializer = HelpDetailSerializer(data=data_raw)  # получить данные в сериализованном виде
            if serializer.is_valid():  # проверка корректности
                serializer.save()  # сохранить данные в сериализованном виде
                return redirect('/accounts/profile/')
                # return Response(status=status.HTTP_201_CREATED)  # success
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # something went wrong...
            '''
        else:
            return render(request, 'register.html', {'form': form})


# User Signin
def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        upass = request.POST.get('password')
        if (email == "") or (upass == ""):
            messages.error(request, 'Пропущен пароль или почта.')
            return redirect('/')

        user = authenticate(email=email, password=upass)
        OtpModel.objects.filter(user=user).delete()
        if user is None:
            messages.error(request, 'Пожалуйста, введите правильные учетные данные.')
            return redirect('/')
        else:
            if user.is_superuser:
                login(request, user)
                return redirect('/')
            else:
                messages.success(request, 'Please verify otp')
                otp_stuff = OtpModel.objects.create(user=user, otp=otp_provider())
                send_otp_in_mail(user, otp_stuff)
                return redirect('/otp/')
    else:
        if request.user.is_authenticated:
            return redirect('/accounts/profile/')
        else:
            return render(request, 'signin.html')


def OtpVerifyView(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        verify_otp = OtpModel.objects.filter(otp=otp)
        if verify_otp.exists():
            login(request, verify_otp[0].user)
            return redirect('/accounts/profile/')
        else:
            messages.error(request, "Invalid otp!")
            return redirect('/otp/')
    else:
        return render(request, 'otp.html')


def activate(request, uidb64, token):
    if request.method == 'GET':
        User = get_user_model()
        try:
            user = User.objects.get(id=uidb64)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Учетная запись успешно подтверждена!')
            return redirect('/')
        else:
            messages.error(request, 'Некорректная ссылка активации!')
        return redirect('/')


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, '🙋‍ You are Successfully Logged Out !')
        return redirect('/')
    else:
        messages.info(request, '☹︎ Please Login First')
    return redirect('/')
