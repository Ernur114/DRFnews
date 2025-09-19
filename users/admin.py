from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Client

@admin.register(Client)
class ClientAdmin(UserAdmin):
    list_display = ("id", "email", "is_active", "is_staff")
    search_fields = ("email",)
    ordering = ("id",)
