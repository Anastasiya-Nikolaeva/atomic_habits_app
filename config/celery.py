import os

from celery import Celery

# Устанавливаем переменную окружения для настройки Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Создаем экземпляр приложения Celery с именем "config"
app = Celery("config")

# Загружаем конфигурацию Celery из настроек Django, используя префикс "CELERY"
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически обнаруживаем задачи в приложениях Django
app.autodiscover_tasks()
