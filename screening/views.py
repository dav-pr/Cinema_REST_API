from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from screening.filters import ScreeningFilter
from screening.models import Movie, ScreeningSession, Screening
from screening.serializers import (
    MovieModelSerializer,
    ScreeningSessionModelSerializer,
    ScreeningModelSerializer,
)


class MovieViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    """
    Це клас ViewSet для моделі Movie, який успадковується від трьох mixins: CreateModelMixin, ListModelMixin,
    RetrieveModelMixin, та від GenericViewSet.

    Цей клас надає базовий набір операцій CRUD (створення, спискування та отримання окремих записів),
    які можна використовувати для взаємодії з об'єктами моделі Movie через API.
    Атрибут queryset визначає, які об'єкти моделі повертаються, тобто, які записи повинні бути доступні через цей
    ViewSet.
    Атрибут serializer_class визначає клас серіалізатора, який використовується для серіалізації та
    десеріалізації об'єктів моделі Movie.
    Атрибут permission_classes визначає, які класи визначають дозволи доступу до цього ViewSet.
    В цьому випадку, доступ до цього ViewSet мають тільки користувачі, які мають права адміністратора,
    оскільки використовується клас IsAdminUser.

    Цей клас можна використовувати для взаємодії з об'єктами моделі Movie через API з використанням стандартних
    HTTP методів, таких як GET, POST, PUT та DELETE.
    """
    serializer_class = MovieModelSerializer
    queryset = Movie.objects.all()
    permission_classes = [
        IsAdminUser,
    ]


class ScreeningSessionViewSet(
    CreateModelMixin,
    GenericViewSet,
):
    queryset = ScreeningSession.objects.all()
    serializer_class = ScreeningSessionModelSerializer
    permission_classes = [IsAdminUser]


class ScreeningViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    queryset = Screening.objects.all()
    serializer_class = ScreeningModelSerializer
    filterset_class = ScreeningFilter
    permission_classes = [IsAuthenticatedOrReadOnly]
