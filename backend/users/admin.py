from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):

    model = User
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("user_type",)}),)


admin.site.register(User, CustomUserAdmin)
