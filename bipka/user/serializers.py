from rest_framework import serializers
from .models import *

#################################################
#                                               #
#              HELP SERIALIZERS                 #
#                                               #
#################################################

class HelpListSerializer(serializers.Serializer):
    class Meta:
        model = Help
        fields = ('title')

class HelpDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'


#################################################
#                                               #
#              USER SERIALIZERS                 #
#                                               #
#################################################

class UserRegSerializer(serializers.Serializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_no', 'head', 'ogrn', 'inn', 'kpp', 'address_reg',
                  'address_fact', 'is_rest', 'is_blago', 'password1', 'password2']
