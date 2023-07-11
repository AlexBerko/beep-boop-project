from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Restaurant)
admin.site.register(Fund)

@admin.register(OtpModel)
class OtpModelAdmin(admin.ModelAdmin):
    list_display = ("created_at", "is_active", "otp", "user", "id")[::-1]
