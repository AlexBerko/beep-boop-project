from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:help_id>/', views.help_list, name='help'),  # read from main page
    re_path(r'^my/helps/(\d+)$', views.help_detail),

    # re_path(r'^api/students/$', views.help_list),  # read from main page
    # also needed read from profile and write/change from profile
    # re_path(r'^api/students/(\d+)$', views.help_detail),
]