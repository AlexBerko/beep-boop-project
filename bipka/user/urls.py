from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LoginView
from django.urls import include
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path('', main_page, name='main_page'),
    path('signin/', SigninView, name='login-user'),
    path('register/', sign_up, name='signup'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('logout/', logoutView, name='logout'),
    path('otp/', OtpVerifyView, name='otp'),
    path("accounts/profile/", OrgDetailView.as_view(), name='home-page'),
    path('help/<int:pk>/', HelpDetailView.as_view(), name='help'),  # <int:pk>
    path('list/', Help_list.as_view(), name='help_list'),  # read from main page
    # path('main/', Help_list.as_view()),
    #re_path(r'^my/helps/(\d+)$', views.help_detail),
    path('create/', ad_create, name='create_help'),
]
