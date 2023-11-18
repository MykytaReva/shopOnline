from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import DailyLetter, User, UserProfile


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "username", "role", "is_active")
    ordering = ("-created_date",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class CustomProfileAdmin(UserAdmin):
    list_display = ("user", "address")
    ordering = ("-created_at",)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, CustomProfileAdmin)
admin.site.register(DailyLetter)
