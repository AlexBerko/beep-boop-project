from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LoginView
from django.urls import include
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path('signin/', SignIN.as_view(), name='login-user'),
    path('register/', SignUP.as_view(), name='signup'),
    path('logout/', LogOUT_API.as_view(), name='user-logout'),
    path('profile/', OrgDetailView.as_view(), name='user-profile'),
    path('otp/', OtpVerifyView_API.as_view(), name='otp'),
    path('activate/<str:uidb64>/<str:token>/', ActivateAccount_API.as_view(), name='activate'),
]
