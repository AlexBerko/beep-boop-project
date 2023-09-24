from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LoginView
from django.urls import include
from rest_framework import routers
from djoser import views as djoser_views

router = routers.DefaultRouter()

urlpatterns = [
    path('register/', SignUP.as_view(), name='signup'),
    path('profile/', OrgDetailView.as_view(), name='user-profile'),
    path('otp/', OtpCheck_API.as_view(), name='otp'),
    path('login/', SignIN_API.as_view(), name='signin'),
    path('<int:pk>/', UserByID_API.as_view(), name='user_id'),

    # path('activate/<str:uidb64>/<str:token>/', ActivateAccount_API.as_view(), name='activate'),
    # path('auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
]
