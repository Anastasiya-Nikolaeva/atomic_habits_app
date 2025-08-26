from celery import shared_task
from drf_yasg.utils import logger

from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def send_message_to_user():
    """
    Отправка уведомлений о выполнении привычки.

    Эта функция проверяет все привычки, которые не являются приятными, и отправляет уведомления
    пользователям о необходимости выполнения привычек. Уведомления отправляются через Telegram.

    Процесс:
    1. Получение всех привычек, которые не являются приятными.
    2. Уменьшение индикатора отправки для каждой привычки.
    3. Если индикатор отправки достигает нуля или меньше, отправляется сообщение пользователю.
    4. Если сообщение успешно отправлено, индикатор отправки сбрасывается на периодичность.
    5. Если у пользователя отсутствует tg_chat_id, записывается предупреждение в лог.
    """
    habits = Habit.objects.filter(sign_of_a_pleasant_habit=False)
    for habit in habits:
        habit.send_indicator -= 1

        if habit.send_indicator <= 0:  # Проверка на ноль или меньше
            if habit.owner.tg_chat_id:
                message = (
                    f"У вас сегодня выполнение привычки: {habit.habit}, "
                    f"которую нужно выполнить в {habit.time_execution} "
                    f"в {habit.place_of_execution}"
                )
                try:
                    send_telegram_message(
                        message=message, chat_id=habit.owner.tg_chat_id
                    )
                except Exception as e:
                    # Логирование ошибки
                    logger.error(f"Ошибка при отправке сообщения: {e}")
                else:
                    habit.send_indicator = habit.periodicity  # Сброс индикатора
            else:
                logger.warning(
                    f"У пользователя {habit.owner.id} отсутствует tg_chat_id."
                )

        habit.save(update_fields=["send_indicator"])
