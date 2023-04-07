"""Модуль містить класи-представлення (views), які взаємодіють з моделями та сервісами додатку purchase."""

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from purchase.models import Order
from purchase.serializers import (
    CartOutputSerializer,
    CreateCartInputSerializer,
    OrderModelSerializer,
)
from purchase.services import (
    add_ticket_to_cart,
    buy_ticket,
    get_buyer_history,
    get_total_spent_amount,
    get_user_cart,
    remove_ticket_from_cart,
    return_purchased_ticket,

)


class OrderViewSet(
    ListModelMixin,
    GenericViewSet,
):
    """
    Клас OrderViewSet.

    Клас OrderViewSet наслідується від ListModelMixin та GenericViewSet і надає декілька API-методів для перегляду
    та керування замовленнями.

    Атрибути класу:
    queryset: запит до бази даних на отримання всіх замовлень.
    serializer_class: клас серіалізатора, який буде використовуватися для перетворення даних замовлення в формат JSON
    та навпаки.
    permission_classes: класи дозволів, які будуть застосовуватися до кожного API-запиту. У цьому випадку тільки
    авентифіковані користувачі матимуть доступ до методів цього класу.
    """

    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def list(self, request, *args, **kwargs):
        """
        Метод list.

        Цей метод належить класу OrderViewSet і реалізує операцію отримання списку замовлень користувача-покупця.
        Параметр buyer цієї операції передається через запит, тому передавати його окремо не потрібно. Отримані
        замовлення серіалізуються за допомогою OrderModelSerializer і повертаються як відповідь на запит у вигляді
        JSON-об'єкту зі списком даних замовлень.
        :param request: вхідний запит
        :return: Response
        """
        orders = get_buyer_history(
            buyer=request.user,
        )
        serializer = self.get_serializer(
            orders,
            many=True,
        )
        return Response(
            serializer.data,
        )

    @action(
        methods=["GET"],
        detail=False,
    )
    def cart(self, request):
        """
        Функція cart.

        Ця функція є декоратором @action, який використовується для створення власного дії в представленні.
        Конкретно цей декоратор створює GET-запит до дії зі списком записів, а не до окремого запису.
        Детальніше, ця дія показує кошик користувача з вже доданими до нього елементами.
        Після отримання запиту, функція використовує метод get_user_cart для отримання списку елементів корзини
        користувача. Потім цей список конвертується у відповідний формат за допомогою серіалізатора
        CartOutputSerializer. Наостанок, функція повертає відповідь зі списком елементів кошика відформатованим
        відповідно до вимог серіалізатора.
        """
        cart = get_user_cart(
            self.request.user,
            self.get_queryset(),
        )
        serializer = CartOutputSerializer(data=cart)
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
        )

    @cart.mapping.post
    def add_to_cart(self, request):
        """
        Функція add_to_cart.

        Ця функція є методом для обробки запитів POST до екшена cart в OrderViewSet. Вона приймає дані запиту у вигляді
        об'єкта запиту, десеріалізує його відповідно до встановлених правил у CreateCartInputSerializer.
        Якщо серіалізатор виконується успішно, функція додає вибраний квиток у кошик користувача, викликаючи функцію
        add_ticket_to_cart, яка використовується для створення нового об'єкта замовлення з операцією
        "додавання у кошик". Функція повертає відповідь сервера зі статусом HTTP 201_CREATED,
        якщо операція виконана успішно.
        """
        serializer = CreateCartInputSerializer(
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)
        add_ticket_to_cart(
            ticket=serializer.validated_data.get("ticket"),
            buyer=self.request.user,
        )
        return Response(
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=["DELETE"],
        detail=True,
    )
    def delete_from_cart(
            self,
            request,
            pk: int,
    ):
        """
        Endpoint delete_from_cart.

        Цей метод є декоратором для видалення квитка з кошика користувача за його ідентифікатором.
        Вхідними параметрами є запит користувача та ідентифікатор замовлення. Метод видаляє замовлення з кошика
        користувача за допомогою функції remove_ticket_from_cart і повертає відповідь з кодом стану
        HTTP 204 NO CONTENT.
        """
        remove_ticket_from_cart(
            buyer=request.user,
            order_id=pk,
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    """
    @extend_schema - це декоратор у фреймворку Django REST Framework (DRF), який дозволяє розширити документацію для
    API використовуючи стандарт OpenAPI/Swagger. Він дозволяє налаштовувати додаткові параметри для документації, такі
    як відповіді, параметри запиту, опис операції тощо.
    Коли додається @extend_schema, він додає нові поля до документації. Наприклад, якщо ми хочемо описати відповіді для
    нашого API, ми можемо використати @extend_schema з параметром responses, який передає словник відповідей з їх
    описом. Після цього, наша документація буде містити ці відповіді для цього API.
    Отже, @extend_schema дозволяє розширити документацію для API використовуючи стандарт OpenAPI/Swagger.
    Він є потужним інструментом для налаштування додаткових параметрів для документації API, які можуть допомогти
    розробникам краще зрозуміти ваш API та його можливості.
    """

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        request=None,
    )
    @action(
        methods=["POST"],
        detail=True,
    )
    def buy_ticket(
            self,
            request,
            pk: int,
    ):
        """
        Endpoint buy_ticket.

        Цей метод дозволяє здійснювати оплату для замовлення з конкретним ідентифікатором. При виклику методу
        передається ідентифікатор замовлення та користувач, який здійснює оплату. Після успішного здійснення оплати,
        метод повертає відповідь зі статусом HTTP 204 No Content.
        """
        buy_ticket(
            pk,
            buyer=request.user,
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
        },
        request=None,
    )
    @action(
        methods=["POST"],
        detail=True,
    )
    def return_ticket(
            self,
            request,
            pk: int,
    ):
        """
        Endpoint return_ticket.

        Endpoint return_ticket повертає квиток після його покупки. Приймає запит на повернення квитка за його унікальним
        ідентифікатором. Викликає функцію return_purchased_ticket з відповідними параметрами. Повертає відповідь
        з HTTP-статусом 204 NO CONTENT.
        """
        return_purchased_ticket(
            order_id=pk,
            buyer=request.user,
        )
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        methods=["GET"],
        detail=False,
    )
    def total_spent_orders(self, request):
        """
        Endpoint total_spent_orders.

        Повертає загальну суму витрачених коштів користувачем на замовлення.
        Аргументи:
        request (HttpRequest): запит, що містить інформацію про користувача.
        Повертає:
        Response: відповідь, що містить словник зі значенням загальної суми витрачених коштів користувачем на
        замовлення.
        """
        total_amount = get_total_spent_amount(
            buyer=request.user,
        )
        return Response(
            {
                "total_spent": total_amount,
            },
        )
