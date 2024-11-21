from django.contrib import admin
from accounts.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'is_active', 'is_staff', 'is_superuser', 'is_deleted')
    search_fields = ('name', 'email')

