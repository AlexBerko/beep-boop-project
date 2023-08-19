import math
import random
from bipka import settings

from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .forms import *
from .token import account_activation_token


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


#@api_view(['POST', 'GET'])
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
