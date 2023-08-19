from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from .models import Help, CustomUser

#################################################
#                                               #
#              HELP SERIALIZERS                 #
#                                               #
#################################################


class HelpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'


class HelpDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'

#################################################
#                                               #
#              USER SERIALIZERS                 #
#                                               #
#################################################

class OrgDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'address_reg',
                  'address_fact', 'is_rest', 'is_ind_pred']
