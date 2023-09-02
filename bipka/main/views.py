import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from .forms import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth import get_user
from rest_framework.authtoken.models import Token

def get_user_from_header(request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        token = auth_header.split(' ')[1]
        if token:
            token_obj = Token.objects.filter(key=token).first()
            if token_obj:
                user = CustomUser.objects.get(id=token_obj.user_id)
                return user
    return None

def main_page(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('http://localhost:3000/login')
            # return redirect('/user/signin/')
        else:
            return redirect("http://localhost:3000/accounts/profile/")
            # return redirect("/user/profile/")


#################################################
#                                               #
#                   HELP VIEWS                  #
#                                               #
#################################################


@permission_classes([IsAuthenticated])
class Help_list(APIView):
    def get(self, request):
        help_objects = Help.objects.filter(is_completed=False, who_complete__isnull=True)
        serializer = HelpListSerializer(help_objects, many=True)
        return Response(serializer.data, status=200)


@permission_classes([IsAuthenticated])
class HelpDetailView(APIView):
    def get(self, request, pk):
        try:
            h = Help.objects.get(id=pk)  # search by id
        except Help.DoesNotExist:
            return Response({'error': 'Просьба с данным id не обнаружена'}, status=400)
        serializer = HelpDetailSerializer(h)
        return Response(serializer.data, status=200)

    def put(self, request, pk):
        try:
            help = Help.objects.get(id=pk)
        except Help.DoesNotExist:
            return Response({'error': 'Просьба с данным id не обнаружена'}, status=400)
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)

        if help.who_asked == current_user:
            data = request.data
            if 'title' in data:
                help.title = data['title']
            if 'full_info' in data:
                help.full_info = data['full_info']
            help.save()
            return Response(status=200)
        else:
            return Response({'error': 'Пользователь не является автором просьбы'}, status=400)

    def post(self, request, pk):
        try:
            help = Help.objects.get(id=pk)
        except Help.DoesNotExist:
            return Response({'error': 'Просьба с данным id не обнаружена'}, status=400)
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)


        if not current_user.is_rest:
            help.is_completed = True
            help.complete_date = timezone.now()
            help.save()
            return Response({'message': 'Просьба успешно выполнена.'}, status=200)
        else:
            help.who_complete = current_user
            help.save()
            return Response({'message': 'Пользователь откликнулся на просьбу.'}, status=200)


    def delete(self, request, pk):
        try:
            help = Help.objects.get(id=pk)
        except Help.DoesNotExist:
            return Response({'error': 'Просьба с данным id не обнаружена'}, status=400)
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)

        if not current_user.is_rest:
            if help.who_asked == current_user:
                help.delete()
                return Response(status=200)
            else:
                return Response({'error': 'Пользователь не является автором просьбы'}, status=400)
        else:
            if help.who_complete == current_user:
                help.who_complete = None
                help.save()
                return Response(status=200)
            else:
                return Response({'error': 'Пользователь не откликался на данную помощь'}, status=400)




@permission_classes([IsAuthenticated])
class AddHelp(APIView):
    def get(self, request):
        return Response(status=200)

    def post(self, request):
        form = HelpForm(request.data)
        if form.is_valid():
            h = form.save(commit=False)

            usr = get_user_from_header(request)
            if not usr:
                return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)
            h.who_asked = usr
            h.save()
            serializer = HelpDetailSerializer(h)
            json = JSONRenderer().render(serializer.data)
            return Response(json, status=200)

        else:
            return Response(form.errors, status=400)

@permission_classes([IsAuthenticated])
class MyHelps(APIView):
    def get(self, request):
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)

        if current_user.is_rest:
            helps = current_user.my_completed.all()
        else:
            helps = current_user.my_requests.all()

        serializer = HelpListSerializer(helps, many=True)
        return Response(serializer.data, status=200)

'''
@permission_classes([IsAuthenticated])
class MyHelps_current(APIView):
    def get(self, request):
        current_user = get_user_from_header(request)
        if not current_user:
            return Response({'error': 'Пользователь c таким токеном не обнаружен'}, status=400)

        if current_user.is_rest:
            helps = current_user.my_completed.filter(is_completed=False)
        else:
            helps = current_user.my_requests.filter(is_completed=False)

        serializer = HelpListSerializer(helps, many=True)
        return Response(serializer.data, status=200)
'''
