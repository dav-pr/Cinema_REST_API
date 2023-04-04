import pytest
from rest_framework import status
from rest_framework.test import APIClient as Client

from screening.models import Screening, Ticket


@pytest.mark.django_db
class TestScreening:
    api_endpoint = "/api/screening/"
    response_date_format = "%Y-%m-%d"
    response_time_format = "%H:%M:%S"

    def test_list_screenings(
        self,
        api_test_client: Client,
        screening_session_screenings: list[Screening],
        tickets: list[Ticket],
    ):
        response = api_test_client.get(
            self.api_endpoint,
        )

        screening = screening_session_screenings[0]
        ticket_ids = screening.tickets.values_list("id", flat=True)
        result = response.json()["results"][0]
        assert response.status_code == status.HTTP_200_OK
        assert result["id"] == screening.id
        assert {ticket["id"] for ticket in result["tickets"]} == set(ticket_ids)
        assert result["available_tickets_count"] == len(ticket_ids)
        assert result[
            "screening_end_time"
        ] == screening.screening_session.end_time.strftime(
            self.response_time_format,
        )
        assert result["screening_date"] == screening.screening_date.strftime(
            self.response_date_format,
        )
