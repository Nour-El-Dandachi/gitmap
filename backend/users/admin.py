from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'role', 'github_login')
    search_fields = ('name', 'email', 'github_login')
    list_filter = ('role',)
