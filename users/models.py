"""Модуль models містить клас User для моделі користувача додатку."""


from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель користувача додатку.

    Атрибути:
    - USERNAME_FIELD: поле, яке використовується як унікальний ідентифікатор користувача (у цьому випадку - email).
    - DEFAULT_BALANCE: значення балансу користувача за замовчуванням.
    - REQUIRED_FIELDS: список полів, які є обов'язковими для створення користувача.

    Поля:
    - email: електронна пошта користувача, що використовується як ідентифікатор.
    - balance: баланс користувача, представлений у вигляді числа з двома знаками після коми.

    Методи:
    - Немає додаткових методів.
    """

    USERNAME_FIELD = "email"
    DEFAULT_BALANCE = 1000
    REQUIRED_FIELDS = ["username"]

    email = models.EmailField(
        unique=True,
    )
    balance = models.DecimalField(
        default=DEFAULT_BALANCE,
        max_digits=6,
        decimal_places=2,
    )
