"""Модуль містить виключення, пов'язані з послугами замовлення.

Включає OrderingServiceError,
який є нащадком класу APIException з бібліотеки rest_framework і використовується для повернення помилок пов'язаних
із замовленнями.
Код статусу HTTP для цієї помилки встановлений на 400 (BAD REQUEST).
"""

from rest_framework import status
from rest_framework.exceptions import APIException


class OrderingServiceError(APIException):
    """
    class OrderingServiceError.

    Цей клас використовується як основа для виключень, які виникають під час обробки запитів у зв'язку з помилками,
    пов'язаними з послугами замовлення. Він наслідується від APIException з бібліотеки rest_framework.exceptions і
    має статус код HTTP 400 (невірний запит).

    APIException є базовим класом виключень для Django Rest Framework API. Він дозволяє створювати спеціалізовані
    виключення для опрацювання винятків, які виникають в процесі роботи з API. Наприклад, при невдалому запиті клієнт
    може отримати відповідь з HTTP-статусом 400 Bad Request, а також повідомлення про те, що запит був неправильним.
    APIException має свою властивість status_code, яка містить HTTP-статус код, пов'язаний з винятком. Доцільно
    використовувати APIException для спеціалізованих виключень, які можуть бути підняті під час обробки запиту.
    """

    status_code = status.HTTP_400_BAD_REQUEST
