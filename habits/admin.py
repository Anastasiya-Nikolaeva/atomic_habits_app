from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Админка модели Habit, позволяющая управлять привычками через интерфейс администратора.

    Атрибуты:
    - list_display: Поля, отображаемые в списке привычек.
    - list_filter: Поля, по которым можно фильтровать привычки.
    - search_fields: Поля, по которым можно выполнять поиск привычек.
    """

    list_display = (
        "id",  # Уникальный идентификатор привычки
        "habit",  # Описание привычки
        "sign_of_a_pleasant_habit",  # Признак приятной привычки
        "related_habit",  # Связанная привычка
        "reward",  # Вознаграждение за выполнение привычки
    )

    list_filter = ("sign_of_a_pleasant_habit",)

    search_fields = ("habit",)
