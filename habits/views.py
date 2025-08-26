from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from habits.models import Habit
from habits.paginations import ViewUserHabitPagination
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для получения списка всех привычек"
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для получения конкретной привычки"
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для создания привычки"
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для обновления информации о привычке"
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для частичного изменения информации о привычке"
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для удаления привычки"
    ),
)
class HabitsViewSet(viewsets.ModelViewSet):
    """
    Представление для модели Habit.

    Этот класс предоставляет стандартные операции CRUD для управления привычками.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = ViewUserHabitPagination

    def perform_create(self, serializer):
        """
        Добавление владельца к Habit при создании и определение поля send_indicator.

        Параметры:
        serializer (HabitSerializer): Сериализатор для создания привычки.
        """
        habit = serializer.save(owner=self.request.user)
        habit.send_indicator = habit.periodicity
        habit.save(update_fields=["send_indicator"])

    def get_permissions(self):
        """
        Определение прав доступа для действий в представлении.

        Возвращает:
        list: Список классов прав доступа для текущего действия.
        """
        if self.action in ["retrieve", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsOwner | IsAdminUser]
        return super().get_permissions()


class UserHabitViewSet(APIView):
    """
    Представление для получения списка всех привычек пользователя.

    Этот класс обрабатывает запросы на получение привычек, принадлежащих текущему пользователю.
    """

    @swagger_auto_schema(responses={200: HabitSerializer()})
    def get(self, request):
        """
        Обработка GET-запроса для получения привычек пользователя.

        Параметры:
        request (Request): HTTP-запрос.

        Возвращает:
        Response: Ответ с пагинированным списком привычек пользователя.
        """
        habits = Habit.objects.filter(owner=request.user)
        paginator = ViewUserHabitPagination()
        result = paginator.paginate_queryset(habits, request)
        serializer = HabitSerializer(result, many=True)
        return paginator.get_paginated_response(serializer.data)


class PublishedHabitListAPIView(generics.ListAPIView):
    """
    Представление для получения списка опубликованных привычек.

    Этот класс обрабатывает запросы на получение привычек, которые опубликованы для общего доступа.
    """

    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(published=True)
    pagination_class = ViewUserHabitPagination
