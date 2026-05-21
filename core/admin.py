from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
# admin.site.register(CustomUser)


@admin.register(CustomUser)
class  CustomUserAdmin(UserAdmin):
    list_display = ['email', 'full_name', 'age', 'gender', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('full_name', 'age', 'gender', 'profile_pic')}),
    )

