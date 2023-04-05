"""
Модуль screening/filters.py.

Модуль filters.py є одним з модулів Django REST Framework (DRF), який використовується для створення фільтрів для
запитів API. DRF надає різноманітні фільтри, які можна використовувати для фільтрації списків об'єктів моделі.
Наприклад, ви можете використовувати фільтри за полями, щоб шукати об'єкти за значеннями певного поля.
Також можна використовувати фільтри за діапазоном, за датою, за ключовими словами тощо.
Модуль filters.py дозволяє створювати користувацькі фільтри для конкретної моделі.
Для цього використовуються класи фільтрів, які успадковуються від базового класу django_filters.FilterSet.
У класі фільтра визначаються поля, за якими можна фільтрувати дані, та логіка фільтрування.
"""

import django_filters
from django_filters import OrderingFilter, rest_framework

from cinema_hall.models import Hall

from screening.models import Screening


class ScreeningFilter(rest_framework.FilterSet):
    """
    Клас ScreeningFilter.

    Клас ScreeningFilter - це набір фільтрів для моделі Screening. Фільтри можуть бути використані для відбору об'єктів
    Screening за певними критеріями.
    Атрибути:
        hall: фільтр по залу, де відбувається сеанс
        start_date: фільтр по даті проведення сеансу
        start_date_gte: фільтр по даті проведення сеансу, яка є більшою або дорівнює вказаній даті
        end_date: фільтр по даті закінчення сеансу
        end_date_lte: фільтр по даті закінчення сеансу, яка є меншою або дорівнює вказаній даті
        start_time: фільтр по часу початку сеансу
        start_time_gte: фільтр по часу початку сеансу, який є більшим або дорівнює вказаному часу
        start_time_lte: фільтр по часу початку сеансу, який є меншим або дорівнює вказаному часу
        o: фільтр для сортування результатів за вказаними полями
    Meta: метадані, які описують, яка модель повинна використовуватись для фільтрації та які поля мають бути доступні
    для фільтрації
    """

    hall = django_filters.ModelChoiceFilter(
        queryset=Hall.objects.all(),
        field_name="screening_session__hall",
        lookup_expr="exact",
    )

    start_date = django_filters.DateFilter(
        field_name="screening_date",
        lookup_expr="exact",
    )
    start_date_gte = django_filters.DateFilter(
        field_name="screening_date",
        lookup_expr="gte",
    )

    end_date = django_filters.DateFilter(
        field_name="screening_session__end_date",
        lookup_expr="exact",
    )
    end_date_lte = django_filters.DateFilter(
        field_name="screening_session__end_date",
        lookup_expr="lte",
    )
    start_time = django_filters.DateFilter(
        field_name="screening_session__start_time",
        lookup_expr="exact",
    )
    start_time_gte = django_filters.DateFilter(
        field_name="screening_session__start_time",
        lookup_expr="gte",
    )
    start_time_lte = django_filters.DateFilter(
        field_name="screening_session__start_time",
        lookup_expr="lte",
    )

    o = OrderingFilter(
        fields=(
            (
                "screening_date",
                "start_date",
            ),
            (
                "screening_session__start_time",
                "start_time",
            ),
            (
                "tickets__price",
                "price",
            ),
        )
    )

    class Meta:
        """
        class Meta класу ScreeningFilter.

        Meta: метадані, які описують, яка модель повинна використовуватись для фільтрації та які поля мають бути
        доступні для фільтрації
        """

        model = Screening
        fields = (
            "hall",
            "start_date",
            "start_date_gte",
            "end_date",
            "end_date_lte",
            "start_time",
            "start_time_gte",
            "start_time_lte",
        )
