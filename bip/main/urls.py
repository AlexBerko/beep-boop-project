from django.urls import path, re_path
from . import views
#Swagger
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="BIP API",
      default_version='v1',
      description='''Restaurants Charity Service
      Documentation could be found [here](/redoc)''',
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="heatherhoneyy@mail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('', views.index, name='index'),
    path('<int:help_id>/', views.help_list, name='help'),  # read from main page
    re_path(r'^my/helps/(\d+)$', views.help_detail),

    # re_path(r'^api/students/$', views.help_list),  # read from main page
    # also needed read from profile and write/change from profile
    # re_path(r'^api/students/(\d+)$', views.help_detail),
    # Swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]