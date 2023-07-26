import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .decorators import *
from .forms import RegisterForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
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
    subject = 'Otp for signin'
    message = f'Hi {user.email}, here we sent otp for secure login \n Otp is - {otp.otp}'
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
        try:
            usr = CustomUser.objects.get(id=9)  # тут поставить id=pk, значения 2 и 9 выдают ответ для тестирования
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # error
        serializer = OrgDetailSerializer(usr)
        json = JSONRenderer().render(serializer.data)
        return Response(json)
    # return render(request, "homePage.html")

@api_view(['POST', 'GET'])
def sign_up(request):
    if request.method == 'GET':  # выводит форму
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
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
        else:
            return render(request, 'register.html', {'form': form})


# User Signin
def SigninView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        upass = request.POST.get('password')
        if (email == "") or (upass == ""):
            messages.error(request, 'Missing email or password')
            return redirect('/')

        user = authenticate(email=email, password=upass)
        OtpModel.objects.filter(user=user).delete()
        if user is None:
            messages.error(request, 'Please Enter Correct Credinatial')
            return redirect('/')
        else:
            # login(request, user)
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
