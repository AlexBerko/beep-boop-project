import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from .forms import *


def main_page(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect('http://localhost:3000/login')
            #return redirect('/signin')
        else:
            return redirect("http://localhost:3000/accounts/profile/")
            #return redirect("/accounts/profile/")


class OrgDetailView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                usr = CustomUser.objects.get(id=request.user.id)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
            serializer = OrgDetailSerializer(usr)
            json = JSONRenderer().render(serializer.data)
            return Response(json)
        else:
            return redirect('/')



def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, '🙋‍ You are Successfully Logged Out !')
        return redirect('/')
    else:
        messages.info(request, '☹︎ Please Login First')
    return redirect('/')


#################################################
#                                               #
#                   HELP VIEWS                  #
#                                               #
#################################################


class Help_list(generics.ListAPIView):
    ''''''
    queryset = Help.objects.all()  # получить список всех просьб
    serializer_class = HelpListSerializer
    '''
    def get(self, request):
        data = Help.objects.all()  # получить список всех просьб
        title = request.query_params.get('title', None)
        if title is not None:
            data = data.filter(title__icontains=title)
        serializer = HelpListSerializer(data, context={'request': self.request}, many=True)  # получить данные в сериализованном виде
        json = JSONRenderer().render(serializer.data)
        # print('/nRESPONSE: %d' %(json))
        return Response(json)  # отправить ответ
    '''


# help list without serializers
# def help_list(request):
#     # return HttpResponse("<h4>Главная сраница</h4>")
#     list_of_helps = Help.objects.all().order_by('-pubdate')
#     return render(request, "index.html", {'list_of_helps': list_of_helps})

class HelpDetailView(APIView):
    def get(self, request, pk):
        try:
            h = Help.objects.get(id=pk)  # search by id
        except Help.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # error
        serializer = HelpDetailSerializer(h)
        json = JSONRenderer().render(serializer.data)
        return Response(json)

    # @method_decorator([login_required, blago_required], name='dispatch')
    def put(self, request, pk):
        json_object = json.loads(request.body)
        data_raw = JSONParser().parse(json_object)  # data after parsing
        serializer = HelpDetailSerializer(data=data_raw, context={'request': request})  # update serialized data
        if serializer.is_valid():  # is it ok?
            serializer.save()  # save
            return Response(status=status.HTTP_204_NO_CONTENT)  # success
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # data is invalid...

    # @method_decorator([login_required, blago_required], name='dispatch')
    def delete(self, request, pk):
        try:
            help = Help.objects.get(id=pk)  # search by id
        except Help.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)  # error
        help.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddHelp(APIView):
    def get(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request):
        form = HelpForm(request.data)
        if form.is_valid():
            h = form.save(commit=False)
            try:
                usr = CustomUser.objects.get(id=request.user.id)  # search by id
                #usr = CustomUser.objects.get(id=2)  # ТЕСТ
            except CustomUser.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
            h.who_asked = usr
            h.save()
            serializer = HelpDetailSerializer(h)
            json = JSONRenderer().render(serializer.data)
            return Response(json)

        else:
            return Response(form.errors, status=400)