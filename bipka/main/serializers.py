from rest_framework import serializers
from .models import Help


class HelpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'


class HelpDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = '__all__'
