import datetime
from django.shortcuts import render
from django.http import HttpResponse, Http404
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from .models import Help
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *

# print list of all helps
def index(request):
    # return HttpResponse("<h4>Главная сраница</h4>")
    list_of_helps = Help.objects.order_by('-pubdate')
    return render(request, "index.html", {'list_of_helps': list_of_helps})

def help(request, help_id):
    try:
        h = Help.objects.get(id=help_id)
    except:
        raise Http404("Страница не найдена!")

    return render(request, "help.html", {'help': h})

# @api_view(['GET'])
def help_list(request):
    if request.method == 'GET':  # получить данные от сервера
        data = Help.objects.all()  # получить список всех просьб
        serializer = HelpSerializer(data, context={'request': request}, many=True)  # получить данные в сериализованном виде
        json = JSONRenderer().render(serializer.data)
        return Response(json)  # отправить ответ

# @api_view('POST')
#  @blago_required
def create_help(request):
    if request.method == 'POST':  # отправить данные на сервер
        print('post')
        name = request.POST['title']
        text = request.POST['full_info']
        elem = Help(title=name, full_info=text, pub_date=datetime.now())
        elem.save()
        data_raw = JSONParser().parse(request.data)  # data after parsing
        serializer = HelpSerializer(data=data_raw)  # получить данные в сериализованном виде
        if serializer.is_valid():  # проверка корректности
            serializer.save()  # сохранить данные в сериализованном виде
            return Response(status=status.HTTP_201_CREATED)  # success
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # something went wrong...


#  @api_view(['PUT', 'DELETE', 'POST'])
def help_detail(request, id):
    try:
        help = Help.objects.get(pk=id)  # search by id
    except Help.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)  # error
    if request.method == 'PUT':  # обновление
        data_raw = JSONParser().parse(request.data)  # data after parsing
        serializer = HelpSerializer(help, data=data_raw, context={'request': request})  # update serialized data
        if serializer.is_valid():  # is it ok?
            serializer.save()  # save
            return Response(status=status.HTTP_204_NO_CONTENT)  # success
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # data is invalid...
    elif request.method == 'DELETE':
        help.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
