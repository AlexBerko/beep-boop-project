from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import CustomUser

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'kpp', 'address_reg',
                  'address_fact', 'is_rest', 'is_blago', 'password1', 'password2']
