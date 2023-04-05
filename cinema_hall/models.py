"""Модуль, що визначає моделі бази даних для додатку cinema."""

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
"""
PhoneNumberField є полем моделі в Django, яке дозволяє зберігати телефонні номери у відповідному форматі.
Модуль phonenumber_field реалізує PhoneNumberField використовуючи бібліотеку Python з назвою phonenumbers,
яка надає функціональність для перевірки та маніпулювання телефонними номерами.
Щоб використовувати PhoneNumberField, спочатку потрібно встановити бібліотеку phonenumbers, виконавши наступну команду:
pip install phonenumbers
"""


class Cinema(models.Model):
    """
    Модель, що представляє кінотеатр.

    Атрибути:
    ----------
    name : CharField Назва кінотеатру.
    address : CharField Адреса кінотеатру.
    phone_number : PhoneNumberField Номер телефону кінотеатру.
    facebook_social_link : URLField Посилання на сторінку кінотеатру в Facebook.
    instagram_social_link : URLField Посилання на сторінку кінотеатру в Instagram.
    youtube_social_link : URLField Посилання на сторінку кінотеатру в YouTube.

    Клас Meta:
    -----------
    unique_together : tuple Кортеж полів, що повинні бути унікальними разом.

    Методи:
    -------
    __str__() -> str
    Повертає рядок з назвою кінотеатру.
    """

    name = models.CharField(
        max_length=128,
    )
    address = models.CharField(
        max_length=256,
    )
    phone_number = PhoneNumberField(
        null=True,
        blank=True,
    )
    facebook_social_link = models.URLField(
        null=True,
        blank=True,
    )
    instagram_social_link = models.URLField(
        null=True,
        blank=True,
    )
    youtube_social_link = models.URLField(
        null=True,
        blank=True,
    )

    class Meta:
        """Метадані."""

        unique_together = (
            "name",
            "address",
        )

    def __str__(self):
        """Повертає рядок з назвою кінотеатру."""
        return self.name


class Hall(models.Model):
    """
    Модель, що представляє зал в кінотеатрі.

    Атрибути:
    ----------
    cinema : ForeignKey
    Кінотеатр, якому належить зал.
    name : CharField Назва залу.

    Клас Meta:
    -----------
    unique_together : tuple Кортеж полів, що повинні бути унікальними разом.

    Методи:
    -------
    __str__() -> str Повертає рядок з назвою залу.
    """

    cinema = models.ForeignKey(
        Cinema,
        related_name="halls",
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=16,
    )

    class Meta:
        """Метадані."""

        unique_together = (
            "name",
            "cinema",
        )

    def __str__(self):
        """Повертає рядок з назвою залу."""
        return self.name


class Seat(models.Model):
    """
    Цей клас Seat є моделлю Django, що представляє місце в залі кінотеатру.

    Він містить наступні атрибути:
    hall: зв'язок з залом, до якого належить місце.
    row: ціле число, що вказує на ряд, в якому знаходиться місце.
    number: ціле число, що вказує на номер місця у ряду.
    Клас Meta містить визначення unique_together, що говорить, що поля hall, row і number повинні бути
    унікальними разом.

    Метод __str__() повертає рядок у вигляді "<ряд - номер>" для даного місця.
    """

    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name="seats",
    )
    row = models.PositiveIntegerField()
    number = models.PositiveIntegerField()

    class Meta:
        """Метадані."""

        unique_together = (
            "hall",
            "row",
            "number",
        )

    def __str__(self):
        """Повертає рядок з характеристиками місця."""
        return f"<{self.row} - {self.number}>"
