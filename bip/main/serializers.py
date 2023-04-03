from rest_framework import serializers
from .models import Help

class HelpSerializer(serializers.Serializer):
    class Meta:
        model = Help
        fields = ('id', 'title', 'full_info', 'org_info', 'pubdate')
