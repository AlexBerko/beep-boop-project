from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:help_id>/', views.help, name='help')
]