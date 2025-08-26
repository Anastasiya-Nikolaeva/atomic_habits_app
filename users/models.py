from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель пользователя.

    Этот класс расширяет стандартную модель пользователя Django,
    заменяя поле username на email в качестве уникального идентификатора.

    Атрибуты:
    - email: Уникальный адрес электронной почты пользователя.
    - first_name: Имя пользователя (необязательное поле).
    - last_name: Фамилия пользователя (необязательное поле).
    - tg_chat_id: ID чата в Telegram для отправки уведомлений (необязательное поле).
    """

    username = None

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        blank=True,
        null=True,
    )
    tg_chat_id = models.PositiveIntegerField(
        verbose_name="ID чата в Telegram",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("id",)

    def __str__(self):
        """Возвращает строковое представление пользователя (email)."""
        return self.email
