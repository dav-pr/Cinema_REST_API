"""Модуль, який містить визначення views для додатку users."""

from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from users.serializers import UserModelSerializer


class UserViewSet(CreateModelMixin, GenericViewSet):
    """Viewset для обробки операцій створення, читання, оновлення та видалення об'єктів користувача.

    Цей viewset успадковується від CreateModelMixin та GenericViewSet, що дозволяє йому надавати такі дії:
    - create: створення нового об'єкта користувача
    - retrieve: отримання певного об'єкта користувача за ID
    - update: оновлення існуючого об'єкта користувача
    - partial_update: часткове оновлення існуючого об'єкта користувача
    - destroy: видалення існуючого об'єкта користувача

    Serializer за замовчуванням, який використовується цим viewset, - UserSerializer, який
    серіалізує об'єкти користувача у формат JSON та навпаки.

    Атрибути:
        serializer_class (Serializer): Serializer за замовчуванням, який використовується цим viewset,
            який конвертує об'єкти користувача у формат JSON та навпаки.
    """

    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserModelSerializer
