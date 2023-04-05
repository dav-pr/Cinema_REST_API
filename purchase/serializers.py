"""
Модуль, який визначає серіалізатори для моделей, що пов'язані з покупками.

Цей модуль визначає серіалізатори для наступних моделей:
- OrderModelSerializer: Серіалізатор для моделі Order.
- TicketModelSerializer: Серіалізатор для моделі Ticket.
- CreateCartInputSerializer: є серіалайзером, який використовується для валідації та серіалізації даних,
    що стосуються створення кошика.
- CartItemTicketOutputSerializer: представлення квитка в одному айтемі замовлення кошику
- CartItemOutputSerializer: представлення айтема кошику
- CartOutputSerializer: представлення кошику
"""

from rest_framework import serializers

from purchase.models import Order

from screening.models import Ticket


class OrderModelSerializer(serializers.ModelSerializer):
    """
    Клас OrderModelSerializer є серіалізатором для моделі Order.

    У Meta класі вказується модель, яку буде серіалізовано, та перелік полів, які будуть включені до серіалізації.
    У даному випадку, fields = "__all__" означає, що будуть включені всі поля моделі. Також в Meta класі вказуються
    поля, які будуть доступні тільки для читання (read-only fields). В даному випадку це "operation", "date" та "buyer".
    """

    class Meta:
        """Meta клас класу OrderModelSerializer."""

        model = Order
        fields = "__all__"
        read_only_fields = (
            "operation",
            "date",
            "buyer",
        )


class TicketModelSerializer(serializers.ModelSerializer):
    """
    Клас TicketModelSerializer.

    Клас TicketModelSerializer є серіалізатором моделі Ticket та містить налаштування для перетворення цієї моделі
    на JSON-об'єкт та навпаки.
    """

    class Meta:
        """Мета клас класу TicketModelSerializer."""

        model = Ticket
        fields = "__all__"


class CreateCartInputSerializer(
    serializers.Serializer,
):
    """
    Клас "CreateCartInputSerializer".

    Клас "CreateCartInputSerializer" є серіалайзером, який використовується для валідації та серіалізації даних,
    що стосуються створення кошика. Він успадковує клас "serializers.Serializer".
    Атрибут "ticket" є полем, яке відповідає за ідентифікатор квитка, який може бути пов'язаний з кошиком.
    Поле дозволяє передавати дані з іншого серіалайзера за допомогою використання первинного ключа
    (PrimaryKeyRelatedField).
    Запит на дані відбувається з усіх об'єктів моделі Ticket (queryset=Ticket.objects.all()), а також дозволяється
    передавати значення null та не є обов'язковим (required=False, allow_null=True).
    """

    ticket = serializers.PrimaryKeyRelatedField(
        queryset=Ticket.objects.all(),
        required=False,
        allow_null=True,
    )


class CartItemTicketOutputSerializer(serializers.Serializer):
    """
    Клас "CartItemTicketOutputSerializer".

    Клас "CartItemTicketOutputSerializer" є серіалайзером, який використовується для серіалізації даних про квиток,
    який знаходиться в кошику. Він успадковує клас "serializers.Serializer".
    Атрибут "id" є цілочисельним полем, яке відповідає за ідентифікатор квитка.
    Атрибут "price" є десятковим числом з фіксованою точністю і максимальною кількістю цифр, що дозволяється
    використовувати до 6 цифр до коми та 2 цифри після коми.
    Атрибут "screening_date_time" є полем дати та часу, яке відображає дату та час показу фільму, на який викуплено
    квиток.
    """

    id = serializers.IntegerField()
    price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    screening_date_time = serializers.DateTimeField()


class CartItemOutputSerializer(
    serializers.Serializer,
):
    """
    Клас "CartItemOutputSerializer".

    Клас "CartItemOutputSerializer" є серіалайзером, який використовується для серіалізації даних про елемент кошику.
    Він успадковує клас "serializers.Serializer".
    Атрибут "id" є цілочисельним полем, яке відповідає за ідентифікатор елемента в кошику.
    Атрибут "ticket" є об'єктом класу "CartItemTicketOutputSerializer".
    """

    id = serializers.IntegerField()
    ticket = CartItemTicketOutputSerializer()


# noinspection PyAbstractClass
class CartOutputSerializer(
    serializers.Serializer,
):
    """Клас "CartOutputSerializer" серіалізатор кошика."""

    items = CartItemOutputSerializer(
        many=True,
    )
    total_price = serializers.FloatField()
