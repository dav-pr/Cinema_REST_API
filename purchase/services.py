"""Модуль містить реалізацію послуг або бізнес-логіки, пов'язаної з додатком purchase."""

from decimal import Decimal

from django.db.models import QuerySet, Sum
from django.utils import timezone

from rest_framework.generics import get_object_or_404

from purchase.errors import OrderingServiceError
from purchase.models import Order
from screening.models import Ticket
from users.models import User


def get_user_cart(
    buyer: User,
    qs: QuerySet,
):
    """Функція для отримання корзини користувача."""
    # запит до бази даних, який повертає список замовлень з корзини користувача.
    added_to_cart_orders = (
        qs.filter(
            buyer=buyer,
            operation=Order.OrderOperation.ADD_TO_CART,
        )
        .select_related(
            "ticket",
        )
        .only(
            "ticket",
            "id",
        )
    )

    # gовертає загальну ціну всіх елементів у кошику користувача.
    total_price = sum(
        Ticket.objects.filter(
            id__in=[i.ticket.id for i in added_to_cart_orders],
        )
        .annotate(total_price=Sum("price"))
        .values_list(
            "total_price",
            flat=True,
        )
    )

    # повертає словник, що містить список елементів у кошику користувача та загальну ціну всіх елементів.
    return {
        "items": [
            {
                "id": i.id,
                "ticket": {
                    "id": i.ticket.id,
                    "price": i.ticket.price,
                    "screening_date_time": i.ticket.screening.screening_date_time,
                },
            }
            for i in added_to_cart_orders
        ],
        "total_price": total_price,
    }


def add_ticket_to_cart(
    buyer: User,
    ticket: Ticket,
) -> Order:
    """Функція додає вибраний квиток до корзини користувача, створюючи нове замовлення."""
    operation = Order.OrderOperation.ADD_TO_CART

    if ticket.is_sold:
        raise OrderingServiceError(
            "Ticket can't be added to cart, it's already sold",
        )

    if timezone.now() > ticket.screening.screening_date_time:
        raise OrderingServiceError(
            "Screening session in past",
        )

    return Order.objects.create(
        buyer=buyer,
        ticket=ticket,
        operation=operation,
    )


def remove_ticket_from_cart(
    buyer: User,
    order_id: int,
):
    """Функція remove_ticket_from_cart видаляє замоллення  із кошика користувача, створюючи нове замовлення."""
    Order.objects.filter(
        id=order_id,
        buyer=buyer,
        operation=Order.OrderOperation.ADD_TO_CART,
    ).delete()


def buy_ticket(
    order_id: int,
    buyer: User,
):
    """Функція buy_ticket реалізує логіку придбання квитка."""
    order = get_object_or_404(
        Order.objects.select_related(
            "ticket",
        ),
        pk=order_id,
    )

    if order.ticket.price > buyer.balance:
        raise OrderingServiceError(
            "insufficient funds",
        )

    if timezone.now() > order.ticket.screening.screening_date_time:
        raise OrderingServiceError("Screening session in past")

    order.operation = order.OrderOperation.PURCHASE
    order.ticket.is_sold = True
    buyer.balance -= order.ticket.price
    order.ticket.save()
    order.save()
    buyer.save()


def get_buyer_history(
    buyer: User,
):
    """Функція get_buyer_history повертає історію покупок."""
    return Order.objects.filter(
        buyer=buyer,
        operation__in=[
            Order.OrderOperation.PURCHASE,
            Order.OrderOperation.RETURN,
        ],
    )


def return_purchased_ticket(
    buyer: User,
    order_id: int,
) -> Order:
    """Функція return_purchased_ticket реалізує повернення квитка."""
    order = get_object_or_404(
        Order.objects.select_related(
            "ticket",
        ),
        pk=order_id,
        buyer=buyer,
        operation=Order.OrderOperation.PURCHASE,
    )

    if Order.objects.filter(
        buyer=buyer,
        ticket=order.ticket,
        operation=Order.OrderOperation.RETURN,
    ).exists():
        raise OrderingServiceError(
            "Ticket is already returned",
        )

    if order.ticket.screening.screening_date_time < timezone.now():
        raise OrderingServiceError(
            "Funds can't be returned. Screening session already started.",
        )

    return_order = Order.objects.create(
        buyer=buyer,
        ticket=order.ticket,
        operation=Order.OrderOperation.RETURN,
    )
    order.ticket.is_sold = False
    buyer.balance += order.ticket.price

    order.save()
    order.ticket.save()
    buyer.save()

    return return_order


def get_total_spent_amount(
    buyer: User,
) -> Decimal:
    """
    Функція get_total_spent_amount.

    Функція призначена для обчислення загальної суми витраченої грошей користувачем на квитки, які він купив.
    Вона використовує модель Order з атрибутом operation, щоб отримати всі замовлення користувача з операцією
    PURCHASE (купівля), тобто всі квитки, які користувач купив. Потім функція викликає метод aggregate моделі Order,
    щоб обчислити загальну суму цін квитків, які користувач купив. Результат повертається як Decimal.
    """
    return Order.objects.filter(
        buyer=buyer,
        operation=Order.OrderOperation.PURCHASE,
    ).aggregate(total_price=Sum("ticket__price"),)["total_price"]
