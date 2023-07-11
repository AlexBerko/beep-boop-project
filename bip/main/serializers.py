from rest_framework import serializers
from .models import Help

class HelpSerializer(serializers.Serializer):
    class Meta:
        model = Help
        fields = ('title')
