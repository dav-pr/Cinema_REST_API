import datetime
from itertools import product
from typing import Any

from django.contrib.auth import get_user_model
from pytest import fixture
from rest_framework.test import APIClient

from cinema_hall.models import Cinema, Hall, Seat
from screening.models import Movie, ScreeningSession, Screening, Ticket

user_model = get_user_model()


@fixture
def test_superuser():
    return get_user_model().objects.create(
        username="test",
        email="test@exmaple.com",
        password="test",
        is_superuser=True,
        is_active=True,
        is_staff=True,
    )


@fixture
def api_test_client(
    test_superuser,
):
    client = APIClient()
    client.force_authenticate(test_superuser)
    return client


@fixture
def cinema_raw():
    return {
        "phone_number": "+380981111111",
        "name": "Cinema",
        "address": "Cinema st.",
        "facebook_social_link": "https://www.facebook.com/my-cinema/",
        "instagram_social_link": "https://www.instagram.com/my-cinema/",
        "youtube_social_link": "https://www.youtube.com/my-cinema/",
    }


@fixture
def cinema(
    cinema_raw,
):
    return Cinema.objects.create(
        **cinema_raw,
    )


@fixture
def hall_raw(
    cinema,
):
    return {
        "cinema": cinema.id,
        "seats_tuple": [
            1,
            2,
        ],
        "name": "First Hall",
    }


@fixture
def hall_with_seats(
    hall_raw,
):
    hall = Hall.objects.create(
        name=hall_raw["name"],
        cinema_id=hall_raw["cinema"],
    )
    seats = []
    for row, seats_count in enumerate(
        hall_raw["seats_tuple"],
        start=1,
    ):
        seats.extend(
            [
                Seat(
                    hall=hall,
                    row=row,
                    number=number,
                )
                for number in range(
                    1,
                    seats_count + 1,
                )
            ]
        )
    Seat.objects.bulk_create(seats)
    return hall


@fixture
def movie_raw():
    return {
        "title": "Movie Title",
        "director": "Test Director",
        "display_format": "2D",
        "release_date": datetime.date(
            year=2000,
            month=1,
            day=1,
        ),
        "description": "Movie description",
        "rent_start_date": datetime.date.today(),
        "rent_end_date": datetime.date.today() + datetime.timedelta(days=14),
        "duration": 60 * 120,
    }


@fixture
def movie(movie_raw):
    return Movie.objects.create(**movie_raw)


@fixture
def screening_session_raw(
    hall_with_seats,
    movie,
):
    return {
        "hall": hall_with_seats.id,
        "movie": movie.id,
        "price": 100,
        "start_time": datetime.time(
            # latest day time, assure
            # that `purchase.services.OrderingServiceError: Screening session in past`
            # not raised when compare timezone.now() > ticket.session_date_time
            # purchase / services.py:66
            hour=23,
            minute=59,
            second=59,
        ),
        "start_date": datetime.date.today(),
        "end_date": datetime.date.today(),
    }


@fixture
def screening_session(
    screening_session_raw,
):
    return ScreeningSession.objects.create(
        hall_id=screening_session_raw["hall"],
        movie_id=screening_session_raw["movie"],
        start_time=screening_session_raw["start_time"],
        start_date=screening_session_raw["start_date"],
        end_date=screening_session_raw["end_date"],
    )


@fixture
def screening_session_screenings_raw(
    screening_session,
) -> list[dict[str, Any]]:
    delta = screening_session.end_date - screening_session.start_date
    return [
        {
            "screening_session": screening_session.id,
            "screening_date": screening_session.start_date
            + datetime.timedelta(
                days=screening_date,
            ),
        }
        for screening_date in range(delta.days + 1)
    ]


@fixture
def screening_session_screenings(
    screening_session_screenings_raw,
):
    screenings = [
        Screening(
            screening_session_id=data["screening_session"],
            screening_date=data["screening_date"],
        )
        for data in screening_session_screenings_raw
    ]
    return Screening.objects.bulk_create(screenings)


@fixture
def tickets_raw(
    screening_session_screenings,
    hall_with_seats,
    screening_session_raw,
):
    return [
        {
            "screening": screening,
            "seat": seat,
            "price": screening_session_raw["price"],
            "is_sold": False,
        }
        for screening, seat in product(
            screening_session_screenings,
            hall_with_seats.seats.all(),
        )
    ]


@fixture
def tickets(
    tickets_raw,
):
    tickets = [Ticket(**data) for data in tickets_raw]
    return Ticket.objects.bulk_create(tickets)
