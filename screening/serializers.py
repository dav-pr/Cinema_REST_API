from datetime import time, datetime, date, timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from screening.models import Movie, ScreeningSession, Screening, Ticket


class MovieModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class TicketModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class ScreeningSessionModelSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(
        write_only=True,
    )

    class Meta:
        model = ScreeningSession
        fields = "__all__"

    @staticmethod
    def _validate_time_intervals_overlap(
        start_time: time,
        end_time: time,
        other_start_time: time,
        other_end_time: time,
    ):
        def _interval_time_to_posix(
            _start_time: time,
            _end_time: time,
        ):
            comparator_start_date = date.today()
            comparator_end_date = date.today()

            if _start_time > _end_time:
                # in case movie ends after midnight
                comparator_end_date = date.today() + timedelta(days=1)

            return int(
                datetime.combine(
                    comparator_start_date,
                    _start_time,
                ).timestamp()
            ), int(
                datetime.combine(
                    comparator_end_date,
                    _end_time,
                ).timestamp()
            )

        start_time_posix, end_time_posix = _interval_time_to_posix(
            start_time,
            end_time,
        )
        other_start_time_posix, other_end_time_posix = _interval_time_to_posix(
            other_start_time,
            other_end_time,
        )

        return (
            start_time_posix <= other_end_time_posix
            and other_start_time_posix <= end_time_posix
        )

    def validate(self, attrs):
        overlap_by_dates_sessions = ScreeningSession.objects.filter(
            hall=attrs["hall"],
            start_date__lte=attrs["end_date"],
            end_date__gte=attrs["start_date"],
        )
        overlap_sessions_time_intervals = [
            (session.start_time, session.end_time)
            for session in overlap_by_dates_sessions
        ]

        # temporary model instance, because
        # end_time is model property
        temp_session_instance = ScreeningSession(
            hall=attrs["hall"],
            movie=attrs["movie"],
            start_time=attrs["start_time"],
            start_date=attrs["start_date"],
            end_date=attrs["end_date"],
        )
        for start_time, end_time in overlap_sessions_time_intervals:
            if self._validate_time_intervals_overlap(
                temp_session_instance.start_time,
                temp_session_instance.end_time,
                start_time,
                end_time,
            ):
                raise ValidationError(
                    {
                        "start_time": [
                            "Session time is already booked",
                        ],
                    },
                )

        if attrs["start_date"] > attrs["end_date"]:
            raise ValidationError(
                {"start_date": "Start date comes after end date"},
            )

        if attrs["start_date"] < attrs["movie"].rent_start_date:
            raise ValidationError(
                {
                    "start_date": (
                        "Screening session start date can't "
                        "be before movie rent start date. "
                    )
                }
            )

        if attrs["end_date"] > attrs["movie"].rent_end_date:
            raise ValidationError(
                {
                    "end_date": (
                        "Screening session end date can't "
                        "be after movie rent end date. "
                    )
                }
            )
        return attrs

    def create(self, validated_data):
        screening_session = ScreeningSession.objects.create(
            hall=validated_data["hall"],
            movie=validated_data["movie"],
            start_time=validated_data["start_time"],
            start_date=validated_data["start_date"],
            end_date=validated_data["end_date"],
        )

        hall_seat_ids = screening_session.hall.seats.values_list(
            "id",
            flat=True,
        )

        # create screening for each screening session
        delta = screening_session.end_date - screening_session.start_date
        for screening_date in range(delta.days + 1):
            screening = Screening.objects.create(
                screening_session=screening_session,
                screening_date=screening_session.start_date
                + timedelta(
                    days=screening_date,
                ),
            )
            tickets = []
            for seat_id in hall_seat_ids:
                tickets.append(
                    Ticket(
                        screening=screening,
                        seat_id=seat_id,
                        price=validated_data["price"],
                        is_sold=False,
                    )
                )

            Ticket.objects.bulk_create(
                tickets,
            )

        return screening_session


class ScreeningModelSerializer(serializers.ModelSerializer):
    available_tickets_count = serializers.IntegerField(
        read_only=True,
    )
    tickets = TicketModelSerializer(
        many=True,
        read_only=True,
    )
    movie = serializers.IntegerField(source="screening_session.movie_id")
    session_end_date = serializers.DateField(source="screening_session.end_date")
    screening_end_time = serializers.TimeField(source="screening_session.end_time")

    class Meta:
        model = Screening
        fields = "__all__"
