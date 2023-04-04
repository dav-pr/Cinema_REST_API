from datetime import date, datetime, timedelta

import pytz
from django.conf import settings
from django.db import models

from cinema_hall.models import Hall, Seat


class Movie(models.Model):
    class MovieDisplayFormat(models.TextChoices):
        THREE_DIMENSION = "3D", "3D"
        TWO_DIMENSION = "2D", "2D"

    title = models.CharField(
        max_length=200,
    )
    director = models.CharField(
        max_length=255,
    )
    display_format = models.CharField(
        max_length=2,
        default=MovieDisplayFormat.TWO_DIMENSION,
        choices=MovieDisplayFormat.choices,
    )
    release_date = models.DateField()
    description = models.TextField()
    poster = models.ImageField(
        upload_to="poster/",
        null=False,
        blank=True,
    )
    age_rating = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    imdb_rating = models.FloatField(
        null=True,
        blank=True,
    )
    imdb_link = models.URLField(
        null=True,
        blank=True,
    )
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    duration = models.PositiveIntegerField()

    class Meta:
        unique_together = (
            "title",
            "director",
            "rent_start_date",
            "rent_end_date",
        )

    def __str__(self):
        return self.title


class ScreeningSession(models.Model):
    session_screening_time: datetime

    hall = models.ForeignKey(
        Hall,
        related_name="screening_sessions",
        on_delete=models.CASCADE,
    )
    movie = models.ForeignKey(
        Movie,
        related_name="screening_sessions",
        on_delete=models.CASCADE,
    )
    start_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()

    @property
    def end_time(self):
        return (
            datetime.combine(
                date.today(),
                self.start_time,
            )
            + timedelta(
                seconds=self.movie.duration + settings.SCREENING_SESSION_BREAK,
            )
        ).time()

    def __str__(self):
        return f"Screening Session: {self.hall.name} {self.start_date} / {self.end_date}: {self.start_time}"


class Screening(models.Model):
    screening_session = models.ForeignKey(
        ScreeningSession,
        related_name="screenings",
        on_delete=models.CASCADE,
    )
    screening_date = models.DateField()

    def __str__(self):
        return f"<Screening: {self.screening_date}>"

    @property
    def screening_date_time(
        self,
    ):
        return datetime.combine(
            self.screening_date,
            self.screening_session.start_time,
            tzinfo=pytz.utc,
        )

    @property
    def available_tickets_count(self):
        return self.tickets.filter(is_sold=False).count()


class Ticket(models.Model):
    screening = models.ForeignKey(
        Screening,
        related_name="tickets",
        on_delete=models.CASCADE,
    )
    seat = models.ForeignKey(
        Seat,
        related_name="seats",
        on_delete=models.CASCADE,
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    is_sold = models.BooleanField(
        default=False,
    )

    class Meta:
        unique_together = (
            "screening",
            "seat",
        )
