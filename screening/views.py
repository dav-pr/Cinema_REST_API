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
