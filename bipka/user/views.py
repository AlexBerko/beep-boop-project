import json

from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from bipka.settings import EMAIL_HOST_USER
from .decorators import *
from .forms import RegisterForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
import math, random
from django.conf import settings
from django.core.mail import send_mail
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from rest_framework import generics
from .token import account_activation_token
from django.core.mail import EmailMessage
import requests
from django.http import JsonResponse


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


#################################################
#                                               #
#                   USER VIEWS                  #
#                                               #
#################################################

class OrgDetailView(APIView):
    def get(self, request):  # тут добавить аргумент pk
        if request.user.is_authenticated:
            try:
                usr = request.user  # тут поставить id=pk, значения 2 и 9 выдают ответ для тестирования
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)  # error
            serializer = OrgDetailSerializer(usr)
            json = JSONRenderer().render(serializer.data)
            return Response(json)
        else:
            return redirect('/signin/')

    # return render(request, "homePage.html")


#@api_view(['POST', 'GET'])
def sign_up(request):
    if request.method == 'GET':  # выводит форму
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.username = user.username.lower()

            ###################################################
            #                   ДОП ЗАДАНИЕ                   #
            ###################################################

            # Проверка, что такая организация существует с помощью стороннего API
            inn = user.inn
            ogrn = user.ogrn
            api_key = 'CAYR4QAsioUmKS5o'
            site = 'company'
            if user.is_ind_pred:
                site = 'entrepreneur'

            is_org_found = False

            response = requests.get(
                'https://api.checko.ru/v2/' + site +'?key=' + api_key + '&inn=' + inn + '&source=true')
            #если запрос завершился успешно
            if response.status_code == 200:
                data = response.json()
                #если отсутствует сообщение об ошибке
                if 'message' not in data['meta']:
                    is_org_found = True

            if not is_org_found:
                response = requests.get(
                    'https://api.checko.ru/v2/' + site + '?key=' + api_key + '&ogrn=' + ogrn + '&source=true')
                if response.status_code == 200:
                    data = response.json()
                    # если есть сообщение об ошибке
                    if 'message' in data['meta']:
                        error_message = 'Не удалось найти организацию с указанными данными!'
                        return render(request, 'register.html', {'form': form, 'error_message': error_message})
                else:
                    error_message = 'Ошибка запроса при поиске организации!'
                    return render(request, 'register.html', {'form': form, 'error_message': error_message})

            data = response.json()
            info = data['data']

            if user.is_ind_pred:
                api_ogrn = info['ОГРНИП']
            else:
                api_ogrn = info['ОГРН']
            api_inn = info['ИНН']

            if api_inn != inn or api_ogrn != ogrn:
                error_message = 'Ошибка! Не удалось найти организацию с текущей комбинацией ИНН и ОГРН.'
                return render(request, 'register.html', {'form': form, 'error_message': error_message})

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

def main_page(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('/signin/')
        else:
            return redirect("/accounts/profile/")


# User Signin
def SigninView(request):
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


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, '🙋‍ You are Successfully Logged Out !')
        return redirect('/')
    else:
        messages.info(request, '☹︎ Please Login First')
    return redirect('/')


#################################################
#                                               #
#                   HELP VIEWS                  #
#                                               #
#################################################


class Help_list(generics.ListAPIView):
    ''''''
    queryset = Help.objects.all()  # получить список всех просьб
    serializer_class = HelpListSerializer
    '''
    def get(self, request):
        data = Help.objects.all()  # получить список всех просьб
        title = request.query_params.get('title', None)
        if title is not None:
            data = data.filter(title__icontains=title)
        serializer = HelpListSerializer(data, context={'request': self.request}, many=True)  # получить данные в сериализованном виде
        json = JSONRenderer().render(serializer.data)
        # print('/nRESPONSE: %d' %(json))
        return Response(json)  # отправить ответ
    '''


# help list without serializers
# def help_list(request):
#     # return HttpResponse("<h4>Главная сраница</h4>")
#     list_of_helps = Help.objects.all().order_by('-pubdate')
#     return render(request, "index.html", {'list_of_helps': list_of_helps})

class HelpDetailView(APIView):
    def get(self, request, pk):
        try:
            h = Help.objects.get(id=pk)  # search by id
        except Help.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # error
        serializer = HelpDetailSerializer(h)
        json = JSONRenderer().render(serializer.data)
        return Response(json)

    # @method_decorator([login_required, blago_required], name='dispatch')
    def put(self, request, pk):
        json_object = json.loads(request.body)
        data_raw = JSONParser().parse(json_object)  # data after parsing
        serializer = HelpDetailSerializer(data=data_raw, context={'request': request})  # update serialized data
        if serializer.is_valid():  # is it ok?
            serializer.save()  # save
            return Response(status=status.HTTP_204_NO_CONTENT)  # success
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # data is invalid...

    # @method_decorator([login_required, blago_required], name='dispatch')
    def delete(self, request, pk):
        try:
            help = Help.objects.get(id=pk)  # search by id
        except Help.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # error
        help.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# help without serializers
# def help(request, name):
#     try:
#         h = Help.objects.get(title__contains=name)
#     except:
#         raise Http404("Страница не найдена!")
#     return render(request, "help.html", {'h': h})

@api_view(['POST', ])
def ad_create(request):
    if request.method == 'POST':
        form = HelpForm(request.POST)
        if form.is_valid():
            h = form.save(commit=False)
            h.pub_date = datetime.date.now()
            # try:
            #     org = CustomUser.objects.get(id=request.user.id)  # search by id
            # except CustomUser.DoesNotExist:
            #     return Response(status=status.HTTP_404_NOT_FOUND)  # error
            # возможно закомменченный вариант лучше
            #            org = request.user  # get_object_or_404(CustomUser, pk=CustomUser.inn)
            # h.org_info = org
            h.save()
        data_raw = JSONParser().parse(request.data)  # data after parsing
        serializer = HelpDetailSerializer(data=data_raw)  # получить данные в сериализованном виде
        if serializer.is_valid():  # проверка корректности
            serializer.save()  # created_by=request.user)  # сохранить данные в сериализованном виде
            return redirect('help', pk=h.id)
            # return Response(status=status.HTTP_201_CREATED)  # success
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # something went wrong...
    else:
        form = HelpForm()
    return render(request, 'create_help.html', {'form': form})
