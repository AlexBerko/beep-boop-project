from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse("<h4>Главная сраница</h4>")
    return render(request, "index.html")
