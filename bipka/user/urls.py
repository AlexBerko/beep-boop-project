from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LoginView


urlpatterns = [
    path("accounts/profile/", homePage, name='home-page'),
    path('', SigninView, name='login-user'),
    path('register/', sign_up, name='signup'),
    path('logout/', logoutView, name='logout'),
    path('otp/', OtpVerifyView, name='otp'),
    path('help/<int:pk>/', HelpDetailView.as_view(), name='help'),  # <int:pk>
    path('list/', Help_list.as_view(), name='help_list'),  # read from main page
    # path('main/', Help_list.as_view()),
    #re_path(r'^my/helps/(\d+)$', views.help_detail),
    path('create/', ad_create, name='create_help'),
]
