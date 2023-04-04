import django_filters
from django_filters import rest_framework, OrderingFilter

from cinema_hall.models import Hall
from screening.models import Screening


class ScreeningFilter(rest_framework.FilterSet):
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
