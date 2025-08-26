from rest_framework import serializers

from habits.serializers import HabitSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.

    Этот класс преобразует экземпляры модели User в JSON-формат и обратно.
    Он также включает связанные привычки пользователя, используя HabitSerializer.

    Атрибуты:
    - habits: Список привычек пользователя, сериализованный с помощью HabitSerializer.
    """

    habits = HabitSerializer(source="users_habits", many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"
