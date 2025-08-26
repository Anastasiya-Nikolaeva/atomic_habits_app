from django.apps import AppConfig


class HabitsConfig(AppConfig):
    """
    Конфигурация приложения 'habits'.

    Атрибуты:
    - default_auto_field: Поле по умолчанию для автоматического создания идентификаторов.
    - name: Имя приложения, используемое в Django.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "habits"
