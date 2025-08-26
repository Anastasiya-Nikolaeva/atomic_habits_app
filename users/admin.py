from django.contrib import admin

from users.models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    """
    Контроллер модели User в админке.

    Этот класс управляет отображением и функциональностью модели User в административной панели Django.
    Позволяет администратору просматривать, фильтровать и искать пользователей.

    Атрибуты:
    - list_display: Поля, отображаемые в списке пользователей.
    - list_filter: Поля, по которым можно фильтровать пользователей.
    - search_fields: Поля, по которым можно выполнять поиск пользователей.
    """

    list_display = ("id", "email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email",)
