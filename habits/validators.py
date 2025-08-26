from datetime import timedelta

from django.core.exceptions import ValidationError


class FieldFillingValidator:
    """
    Проверка заполнения полей reward и related_habit

    Этот валидатор гарантирует, что только одно из полей (reward или related_habit) заполнено,
    и что у приятной привычки не может быть связанной привычки или вознаграждения.
    """

    def __init__(self, reward, related_habit, sign_of_a_pleasant_habit):
        self.reward = reward
        self.related_habit = related_habit
        self.sign_of_a_pleasant_habit = sign_of_a_pleasant_habit

    def __call__(self, instance):
        """
        Проверяет заполнение полей в экземпляре модели.

        Параметры:
        instance (Model): Экземпляр модели, который проверяется.

        Исключения:
        ValidationError: Если условия валидации не выполнены.
        """

        reward_field = getattr(instance, self.reward, None)
        related_habit_field = getattr(instance, self.related_habit, None)
        sign_of_a_pleasant_habit_field = getattr(
            instance, self.sign_of_a_pleasant_habit, None
        )

        if reward_field and related_habit_field:
            raise ValidationError(
                "Может быть заполнено поле reward или поле related_habit, но не оба."
            )
        if sign_of_a_pleasant_habit_field:
            if reward_field or related_habit_field:
                raise ValidationError(
                    "У приятной привычки не может быть связанной привычки или вознаграждения."
                )
        else:
            if not reward_field and not related_habit_field:
                raise ValidationError(
                    "Поле reward или поле related_habit обязательно для заполнения у полезной привычки."
                )


class RelatedHabitValidator:
    """
    Валидатор для проверки связанной привычки на принадлежность к приятной привычке.

    Этот валидатор гарантирует, что связанная привычка является приятной.
    """

    def __init__(self, related_habit):
        self.related_habit = related_habit

    def __call__(self, instance):
        """
        Проверяет, является ли связанная привычка приятной.

        Параметры:
        instance (Model): Экземпляр модели, который проверяется.

        Исключения:
        ValidationError: Если связанная привычка не является приятной.
        """

        habit = getattr(instance, self.related_habit)
        if habit and not habit.sign_of_a_pleasant_habit:
            raise ValidationError("Связанная привычка должна быть приятной.")


def execution_time_validator(value):
    """
    Валидатор для проверки продолжительности выполнения привычки.

    Проверяет, что продолжительность выполнения привычки не превышает 120 секунд.

    Параметры:
    value (timedelta): Продолжительность выполнения привычки.

    Исключения:
    ValidationError: Если продолжительность превышает 120 секунд.
    """

    if value and value > timedelta(seconds=120):
        raise ValidationError(
            "Продолжительность выполнения привычки не может быть более 120 секунд."
        )
