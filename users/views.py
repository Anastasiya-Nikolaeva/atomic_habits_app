from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from users.models import User
from users.serializers import UserSerializer


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для получения списка всех пользователей"
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для получения конкретного пользователя"
    ),
)
@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для создания пользователя"
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для обновления информации о пользователе"
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для частичного изменения информации о пользователе"
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        operation_description="Контроллер для удаления пользователя"
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    Представление для модели User.

    Этот класс предоставляет стандартные операции CRUD для управления пользователями.
    Доступ к созданию пользователей открыт для всех, в то время как другие действия
    доступны только администраторам.

    Атрибуты:
    - serializer_class: Сериализатор, используемый для преобразования данных пользователя.
    - queryset: Набор данных пользователей, доступных для операций.
    - permission_classes: Классы разрешений, определяющие доступ к действиям.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        """
        Определяет права доступа для действий в представлении.

        Если действие - создание пользователя, разрешения устанавливаются на AllowAny,
        что позволяет любому пользователю создавать новых пользователей.

        Возвращает:
        list: Список классов прав доступа для текущего действия.
        """
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Выполняет логику создания нового пользователя.

        Устанавливает пользователя как активного и хэширует пароль перед сохранением.

        Параметры:
        serializer (UserSerializer): Сериализатор для создания пользователя.
        """
        user = serializer.save(is_active=True)
        user.set_password(user.password)  # Хэширует пароль
        user.save(update_fields=["password"])  # Сохраняет только поле пароля
