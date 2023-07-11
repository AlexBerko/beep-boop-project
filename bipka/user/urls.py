from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("accounts/profile/", homePage, name='home-page'),
    path('', SigninView, name='login-user'),
    path('register/', sign_up, name='signup'),
    path('logout/', logoutView, name='logout'),
    path('otp/', OtpVerifyView, name='otp'),

]
