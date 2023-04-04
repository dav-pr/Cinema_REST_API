from typing import Any

import pytest
from rest_framework import status
from rest_framework.test import APIClient as Client

from cinema_hall.models import Hall


@pytest.mark.django_db
class TestHall:
    api_endpoint = "/api/hall/"

    def test_create_hall(
        self,
        api_test_client: Client,
        hall_raw: dict[str, Any],
    ):
        response = api_test_client.post(
            self.api_endpoint,
            data=hall_raw,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_list_hall(
        self,
        api_test_client: Client,
        hall_with_seats: Hall,
    ):
        response = api_test_client.get(
            self.api_endpoint,
        )

        assert response.json()["results"] == [
            {
                "id": hall_with_seats.id,
                "cinema": hall_with_seats.cinema_id,
                "name": hall_with_seats.name,
                "seats": [
                    {
                        "id": seat.id,
                        "number": seat.number,
                        "row": seat.row,
                    }
                    for seat in hall_with_seats.seats.iterator()
                ],
            },
        ]
