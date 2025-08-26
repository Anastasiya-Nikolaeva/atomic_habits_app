from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.views import HabitsViewSet, PublishedHabitListAPIView, UserHabitViewSet

app_name = HabitsConfig.name

# Создание маршрутизатора для управления URL-адресами
router = DefaultRouter()
router.register(r"habits", HabitsViewSet, basename="habits")

urlpatterns = [
    path("user-habits-list/", UserHabitViewSet.as_view(), name="user_habits_list"),
    path(
        "user-habits-list-published/",
        PublishedHabitListAPIView.as_view(),
        name="user_habits_list_published",
    ),
] + router.urls
