from rest_framework import serializers
from .models import Help


class HelpListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ['id', 'title', 'full_info', 'pub_date', 'is_completed', 'who_asked_id', 'who_complete_id',
        'deadline_date', 'is_taken']


class HelpDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ['id' 'title', 'full_info', 'pub_date', 'is_completed', 'who_asked_id', 'who_complete_id',
        'deadline_date', 'is_taken']
