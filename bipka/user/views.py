from .forms import RegisterForm
from django.shortcuts import render, redirect
from .models import OtpModel
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import math, random
from django.conf import settings
from django.core.mail import send_mail


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

def homePage(request):
    return render(request, "homePage.html")

def sign_up(request):
        if request.method == 'GET':
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
                return redirect('/accounts/profile/')
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
        print(user)
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