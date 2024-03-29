from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import TelegramAccount, CustomUser

admin.site.register(TelegramAccount)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                "username",
                "password",
            ),
        }),
        ("Personal info", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "telegram_account",
            ),
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important dates", {
            "fields": (
                "last_login",
                "date_joined",
            ),
        }),
    )
