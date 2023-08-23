from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LoginView
from django.urls import include
from rest_framework import routers


router = routers.DefaultRouter()

urlpatterns = [
    path('', main_page, name='main_page'),
    path('help/<int:pk>/', HelpDetailView.as_view(), name='help_info'),
    path('help/list/', Help_list.as_view(), name='help_list'),  # read from main page
    #re_path(r'^my/helps/(\d+)$', views.help_detail),
    path('help/create/', AddHelp.as_view(), name='create_help'),
]
