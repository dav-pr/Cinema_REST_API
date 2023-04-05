"""Модуль apps.py дозволяє налаштовувати параметри конфігурації додатку."""
from django.apps import AppConfig


class PurchaseConfig(AppConfig):
    """
    Клас PurchaseConfig.

    Клас PurchaseConfig є підкласом django.apps.AppConfig і використовується для конфігурації додатку purchase.
    Використовуйте BigAutoField замість звичайного автоінкрементного поля AutoField, якщо ви очікуєте багато записів
    в таблиці бази даних. BigAutoField зберігає значення більшого діапазону, ніж AutoField, що дозволяє вам зберігати
    значення ідентифікаторів для більшої кількості записів в таблиці. Якщо ви очікуєте, що ваша таблиця міститиме
    більше, ніж 2 мільярди записів, то використання BigAutoField буде обов'язковим. Проте, слід пам'ятати, що це займе
    більше місця в базі даних, ніж звичайний AutoField.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "purchase"
