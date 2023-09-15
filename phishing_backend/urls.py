from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView
from django.urls import include
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
   path('phishing/', Phishing.as_view(), name='evil_phishing'),
]
