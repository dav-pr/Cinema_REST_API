"""Модуль, що визначає моделі бази даних для додатку purchase."""

from django.contrib.auth import get_user_model
from django.db import models

from screening.models import Ticket


class Order(models.Model):
    """
    Клас Order відображає замовлення квитка на фільм.

    Кожен об'єкт класу зберігає інформацію про покупця, квиток,
    операцію замовлення та дату створення.
    Атрибути:
        buyer: покупець квитка
        ticket: квиток, який був замовлений
        operation: тип операції замовлення (покупка, додавання в кошик, повернення)
        date: дата створення замовлення
    Атрибути Meta:
        unique_together: список полів, які повинні бути унікальними разом. У цьому випадку - комбінація полів "buyer",
        "ticket" та "operation".
    У моделі Order використовуються ForeignKey, які вказують на інші моделі. Коли ви видаляєте об'єкт, на який
    посилається ForeignKey, Django повинен виконати дію, щоб зберегти цілісність даних. on_delete=models.CASCADE
    означає, що при видаленні пов'язаного об'єкта, залежні об'єкти будуть також видалені
    (в даному випадку, якщо видалити User, який є покупцем квитка, то всі його замовлення також будуть видалені).
    """

    class OrderOperation(models.TextChoices):
        """
        Клас OrderOperation.

        Клас OrderOperation є підкласом models.TextChoices з визначенням можливих значень для поля operation
        моделі Order.
        Атрибути цього класу визначають допустимі значення для operation та їхнє відображення в адміністративному
        інтерфейсі та інших джерелах відображення.
        """

        PURCHASE = "PR", "Purchase"
        ADD_TO_CART = "CT", "Add to cart"
        RETURN = "RT", "Return"

    buyer = models.ForeignKey(
        get_user_model(),
        related_name="orders",
        on_delete=models.CASCADE,
    )
    ticket = models.ForeignKey(
        Ticket,
        related_name="orders",
        on_delete=models.CASCADE,
    )
    operation = models.CharField(
        max_length=2,
        choices=OrderOperation.choices,
    )
    date = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        """Забезпечує унікальність набора полів."""

        unique_together = (
            "buyer",
            "ticket",
            "operation",
        )
