from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitTest(APITestCase):
    """
    Тестирование API для модели Habit
    """

    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.habit = Habit.objects.create(
            habit="test полезная привычка",
            place_of_execution="test место",
            time_execution="12:00",
            reward="test вознаграждение",
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_retrieve_habit(self):
        """
        Получение конкретной привычки
        """
        url = reverse("habits:habits-detail", kwargs={"pk": self.habit.pk})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json()["habit"], "test полезная привычка")

    def test_delete_habit(self):
        """
        Удаление привычки
        """
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)
