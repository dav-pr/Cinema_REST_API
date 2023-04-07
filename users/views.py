"""Модуль, який містить визначення views для додатку users."""

from django.contrib.auth import get_user_model


from drf_spectacular.utils import extend_schema

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404

from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.serializers import UserModelSerializer, RefreshTokenSerializer


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

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [
                permissions.AllowAny,
            ]
        else:
            permission_classes = [
                permissions.IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]

    @action(
        detail=False,
        methods=["GET"],
    )
    def retrieve_self(self, request, *args, **kwargs):
        instance = get_object_or_404(
            self.model.objects.all(),
            pk=request.user.id,
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

# реалізація логаута

@extend_schema(
        request=RefreshTokenSerializer,
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
    )
    @action(
        detail=False,
        methods=["POST"],
    )
    def logout(
        self,
        request,
        *args,
        **kwargs,
    ):
        serializer = RefreshTokenSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )
        serializer.save()
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )