from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'website_url', 'last_name', 'first_name', 'is_active', 'is_staff', 'is_superuser' ]
