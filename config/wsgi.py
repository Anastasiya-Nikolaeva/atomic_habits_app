import os

from django.core.wsgi import get_wsgi_application

# Устанавливаем переменную окружения для указания настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Получаем WSGI-приложение для работы с Django
application = get_wsgi_application()
