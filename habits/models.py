from django.conf import settings
from django.db import models
from datetime import timedelta
from django.core.validators import MaxValueValidator

from habits.validators import FieldFillingValidator, RelatedHabitValidator, execution_time_validator


class Habit(models.Model):
    """
    Модель привычки
    """

    habit = models.CharField(max_length=255, verbose_name="Привычка")
    place_of_execution = models.CharField(
        max_length=255,
        verbose_name="Место выполнения привычки",
        null=True,
        blank=True
    )
    time_execution = models.TimeField(
        verbose_name="Время выполнения привычки",
        null=True,
        blank=True
    )
    periodicity = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(7)],
        verbose_name="Периодичность привычки",
        default=1,
    )
    time_to_complete = models.DurationField(
        default=timedelta(seconds=120),
        verbose_name="Продолжительность выполнения привычки",
    )
    sign_of_a_pleasant_habit = models.BooleanField(
        verbose_name="Показатель приятной привычки",
        default=False
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        verbose_name="Связанная приятная привычка",
        null=True,
        blank=True,
        related_name="related_habits",
    )
    reward = models.CharField(
        verbose_name="Вознаграждение за привычку",
        max_length=255,
        null=True,
        blank=True
    )

    class Status(models.TextChoices):
        PUBLISHED = "Опубликован", "Опубликован"
        UNPUBLISHED = "Не опубликован", "Не опубликован"

    published = models.CharField(
        max_length=50,
        choices=Status.choices,
        default=Status.UNPUBLISHED,
        verbose_name="Статус опубликования привычки",
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Создатель привычки",
        related_name="users_habits",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ("id",)

    def clean(self):
        # Вызов валидаторов
        FieldFillingValidator("reward", "related_habit", "sign_of_a_pleasant_habit")(
            self
        )
        RelatedHabitValidator("related_habit")(self)
        execution_time_validator(self.time_to_complete)

    def __str__(self):
        return self.habit
