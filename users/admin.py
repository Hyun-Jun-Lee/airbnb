from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    # UserAdmin에서 기본 제공하는 fieldset에 User 모델에서 정의한 필드 추가
    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": (
                    "avatar",
                    "gender",
                    "bio",
                    "birth",
                    "language",
                    "currency",
                    "superhost",
                    "login_method",
                )
            },
        ),
    )
    # UserAdmin.list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    list_filter = UserAdmin.list_filter + ("superhost",)

    # UserAdmin.list_display = ("username", "email", "first_name", "last_name", "is_staff")
    list_display = UserAdmin.list_display + (
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "login_method",
    )

    ordering = [
        "-id",
    ]
