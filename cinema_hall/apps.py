"""Модуль cinema/apps.py дозволяє налаштовувати параметри конфігурації додатку."""

from django.apps import AppConfig


class CinemaHallConfig(AppConfig):
    """
    Цей клас CinemaHallConfig є нащадком класом AppConfig для Django-додатку з назвою cinema_hall.

    Він містить два атрибути:
    default_auto_field: Це рядок, який визначає значення за замовчуванням для автоматичного поля у моделях додатку.
    У цьому випадку він встановлений на "django.db.models.BigAutoField", що означає, що додаток буде використовувати
    великий цілий тип для первинних ключів за замовчуванням.
    name: Це назва додатку.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "cinema_hall"
