from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфигурация приложения 'users'.

    Этот класс настраивает параметры приложения, связанные с пользователями,
    включая использование поля по умолчанию для автоматического создания идентификаторов.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
