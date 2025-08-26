from rest_framework import serializers

from habits.models import Habit
from habits.validators import FieldFillingValidator, execution_time_validator


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit.

    Этот сериализатор преобразует экземпляры модели Habit в JSON-формат и обратно.
    Он также выполняет валидацию данных перед сохранением.
    """

    time_to_complete = serializers.DurationField(
        validators=[execution_time_validator], required=False
    )

    class Meta:
        model = Habit
        exclude = ()
        validators = [
            FieldFillingValidator(
                "reward", "related_habit", "sign_of_a_pleasant_habit"
            ),
        ]
        read_only_fields = ()

    def validate(self, attrs):
        """
        Дополнительная валидация атрибутов сериализатора.

        Этот метод может быть переопределен для добавления пользовательской логики валидации.

        Параметры:
        attrs (dict): Атрибуты, переданные для валидации.

        Возвращает:
        dict: Валидация успешна, возвращает атрибуты.
        """
        return super().validate(attrs)
