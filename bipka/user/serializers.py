from rest_framework import serializers
from .models import CustomUser

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'address_reg',
                  'address_fact', 'is_rest', 'is_ind_pred', 'password']

class OrgDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'address_reg',
                  'address_fact', 'is_rest', 'is_ind_pred']