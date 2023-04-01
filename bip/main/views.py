from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Help

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
