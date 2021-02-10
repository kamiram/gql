from django.contrib import admin
from .models import ApiUser


class ApiUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(ApiUser, ApiUserAdmin)
