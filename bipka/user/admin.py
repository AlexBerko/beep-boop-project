from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Restaurant)
admin.site.register(Fund)
admin.site.register(Help)

@admin.register(OtpModel)
class OtpModelAdmin(admin.ModelAdmin):
    list_display = ("created_at", "is_active", "otp", "user", "id")[::-1]
