from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания суперадмина.

    Эта команда создает нового пользователя с правами суперадминистратора.
    Суперадминистратор имеет доступ ко всем функциям административной панели Django.
    """

    def handle(self, *args, **options):
        """
        Выполняет логику создания суперадминистратора.

        Создает пользователя с заданными параметрами и устанавливает пароль.

        Параметры:
        *args: Позиционные аргументы, переданные команде.
        **options: Опции, переданные команде.

        Примечание:
        Пароль по умолчанию установлен на "123qwe". Рекомендуется изменить его после первого входа.
        """
        user = User.objects.create(
            email="admin@sky.ru",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password("123qwe")
        user.save()
