"""
Модуль apps.py дозволяє налаштовувати параметри конфігурації додатку.

Дозволяє налаштовувати параметри такі параметри як назва, версія, URL-адреса місця знаходження шаблонів тощо.
"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфігураційний клас для додатку "users" в Django.

    Attributes:
        default_auto_field (str): Назва поля для автоматичної генерації первинного ключа.
        name (str): Назва додатку.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
