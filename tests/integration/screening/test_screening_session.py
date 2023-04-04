import datetime
from typing import Any

import pytest
from rest_framework import status
from rest_framework.test import APIClient as Client

from screening.models import ScreeningSession, Screening


@pytest.mark.django_db
class TestScreeningSession:
    api_endpoint = "/api/screening_session/"
    response_date_format = "%Y-%m-%d"
    response_time_format = "%H:%M:%S"

    def test_create_screening_session(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data=screening_session_raw,
        )
        ss_id = response.json()["id"]

        assert response.status_code == status.HTTP_201_CREATED
        assert ScreeningSession.objects.filter(
            id=ss_id,
        ).exists()

    def test_create_screening_session_additional_entities_created(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data=screening_session_raw,
        )
        ss_id = response.json()["id"]

        ss = ScreeningSession.objects.get(
            id=ss_id,
        )
        session_days_delta = ss.end_date - ss.start_date
        earliest_screening = ss.screenings.all().earliest("screening_date")
        latest_screening = ss.screenings.all().latest("screening_date")
        # screenings created for each session day
        assert ss.screenings.count() == session_days_delta.days + 1
        assert earliest_screening.screening_date == ss.start_date
        assert latest_screening.screening_date == ss.end_date

        # each screening has tickets
        hall_seat_ids = ss.hall.seats.values_list(
            "id",
            flat=True,
        )
        for screening in ss.screenings.iterator():
            screening: Screening
            assert screening.tickets.filter(
                screening=screening,
                seat_id__in=hall_seat_ids,
                price=screening_session_raw["price"],
                is_sold=False,
            ).count() == len(hall_seat_ids)

    def test_create_screening_session_failed_overlap_by_start_time(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        ScreeningSession.objects.create(
            hall_id=screening_session_raw["hall"],
            movie_id=screening_session_raw["movie"],
            start_time=datetime.time(
                hour=1,
                minute=0,
                second=0,
            ),
            start_date=screening_session_raw["start_date"],
            end_date=screening_session_raw["end_date"],
        )
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "start_time": datetime.time(
                    hour=1,
                    minute=0,
                    second=0,
                ),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"start_time": ["Session time is already booked"]}

    def test_create_screening_session_failed_overlap_by_end_time(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        ScreeningSession.objects.create(
            hall_id=screening_session_raw["hall"],
            movie_id=screening_session_raw["movie"],
            start_time=datetime.time(
                hour=1,
                minute=0,
                second=0,
            ),
            start_date=screening_session_raw["start_date"],
            end_date=screening_session_raw["end_date"],
        )
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "start_time": datetime.time(
                    hour=0,
                    minute=59,
                    second=59,
                ),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"start_time": ["Session time is already booked"]}

    def test_create_screening_session_failed_movie_rent_is_not_started(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
        movie_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "start_date": movie_raw["rent_start_date"] - datetime.timedelta(days=1),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "start_date": [
                "Screening session start date can't be before movie rent start date. "
            ]
        }

    def test_create_screening_session_failed_movie_rent_is_over(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
        movie_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "end_date": movie_raw["rent_end_date"] + datetime.timedelta(days=1),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "end_date": [
                "Screening session end date can't be after movie rent end date. "
            ]
        }

    def test_create_screening_session_failed_start_date_comes_after_end_date(
        self,
        api_test_client: Client,
        screening_session_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data={
                **screening_session_raw,
                "start_date": screening_session_raw["end_date"],
                "end_date": screening_session_raw["start_date"]
                - datetime.timedelta(
                    days=7,
                ),
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"start_date": ["Start date comes after end date"]}

    def test_screening_session_correct_calculates_end_date_property(
        self,
        screening_session,
        movie_raw: dict[str, Any],
        settings,
    ):
        assert (
            screening_session.end_time
            == (
                datetime.datetime.combine(
                    datetime.date.today(),
                    screening_session.start_time,
                )
                + datetime.timedelta(
                    seconds=screening_session.movie.duration
                    + settings.SCREENING_SESSION_BREAK,
                )
            ).time()
        )
