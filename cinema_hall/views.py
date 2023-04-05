"""
Модуль cinema_hall/views.py.

Класи та функції в модулі cinema_hall/views.py використовуються для взаємодії з API для кінотеатру, а саме з моделями
Cinema та Hall.
"""

from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from cinema_hall.models import Cinema, Hall
from cinema_hall.serializers import (
    CinemaModelSerializer,
    HallModelSerializer,
)


class CinemaViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    """
    клас CinemaViewSet.

    Цей клас є підкласом GenericViewSet, який включає в себе кілька міксинів: CreateModelMixin, ListModelMixin та
    RetrieveModelMixin. Використовуючи цей клас, можна створити ендпойнти для створення, списку та отримання даних
    про кінотеатри.

    Атрибути:
    queryset: Запит, що вибирає всі кінотеатри.
    serializer_class: Клас серіалізатора, який використовується для серіалізації/десеріалізації моделей.
    permission_classes: Список класів, які перевіряють дозвіл на доступ до ресурсу.

    Методи:
    create(self, request, *args, **kwargs): Створює новий кінотеатр на основі наданих даних у запиті.
    list(self, request, *args, **kwargs): Повертає список усіх кінотеатрів.
    retrieve(self, request, *args, **kwargs): Повертає інформацію про окремий кінотеатр за заданим ідентифікатором.
    Даний клас підлягає перевірці дозволу на доступ до ресурсу, що робить його доступним лише для користувачів
    з правами адміністратора.
    """

    queryset = Cinema.objects.all()
    serializer_class = CinemaModelSerializer
    permission_classes = [
        IsAdminUser,
    ]


class HallViewSet(
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    """
    Клас HallViewSet.

    Клас HallViewSet є нащадком класів  GenericViewSet, CreateModelMixin, ListModelMixin, RetrieveModelMixin,
    GenericViewSet, та містить методи для створення, спискування та отримання даних для сутності Hall.
    Він також містить permission_classes, які обмежують доступ до даних для залогінених адміністраторів.

    GenericViewSet є класом перегляду Django REST Framework, який забезпечує базовий інтерфейс для реалізації
    переглядів API. Він поєднує дві інших класи перегляду: APIView, який забезпечує розширення функціональності Django,
    і ViewSet, який забезпечує підтримку дій CRUD (створення, отримання, оновлення та видалення) для моделі.
    Клас GenericViewSet надає методи, такі як list(), create(), retrieve(), update(), partial_update() та destroy(),
    які можна використовувати для реалізації переглядів API залежно від потреб проекту. Він також забезпечує підтримку
    різних типів запитів HTTP, таких як GET, POST, PUT, PATCH та DELETE.

    CreateModelMixin - це mixin (змішувач) для Django REST Framework, який додає підтримку HTTP запитів для створення
    ресурсів. Змішувач додає реалізацію методу create для APIView, який дозволяє створювати нові записи у базі даних на
    основі даних, які надсилаються у POST запиті.
    Для використання CreateModelMixin потрібно додати його до класу відображення (view), який використовується в
    Django REST Framework, а також встановити параметр serializer_class, який вказує, який серіалізатор повинен
    використовуватися для створення нових ресурсів.
    CreateModelMixin також додає можливість налаштувати логіку після успішного створення ресурсу за допомогою методу
    perform_create.

    ListModelMixin - це клас, що надає методи для списку об'єктів моделі (моделей), що підтримує CRUD (створення,
    отримання, оновлення, видалення).
    Цей клас містить два методи:
    list(self, request, *args, **kwargs): повертає список об'єктів моделі, представлених у вигляді JSON або іншого
    формату відповідно до запиту клієнта.
    get_queryset(self): повертає запит на вибірку всіх об'єктів моделі, які відображаються в методі list.
    ListModelMixin не надає методи для створення, оновлення та видалення об'єктів моделі, він тільки додає можливість
    перегляду списку об'єктів. Для цього потрібно використовувати спеціальні класи, які додають ці функції до
    ListModelMixin, наприклад CreateModelMixin, UpdateModelMixin, DestroyModelMixin тощо.

    RetrieveModelMixin є одним з міксінів в Django REST Framework, який дозволяє додаткові операції над моделлю,
    такі як отримання окремого запису. Клас додає HTTP метод GET, який дозволяє отримати детальну інформацію про об'єкт
    з використанням ідентифікатора запису в URL.
    RetrieveModelMixin вимагає визначення queryset та serializer_class, а також передається в GenericAPIView, щоб
    включити HTTP GET запит для одного об'єкту в API. Він також включає додаткові методи для забезпечення коректної
    поведінки серіалізатора та обробки помилок.


    Атрибути:
    queryset: запит на отримання всіх залів.
    serializer_class: серіалізатор, який використовується для конвертації даних у формат JSON та навпаки.
    permission_classes: список дозволених класів перевірки прав доступу.
    Методи:
    create(): створення нового об'єкту Hall на основі переданих даних.
    list(): отримання списку всіх залів.
    retrieve(): отримання конкретного залу за його унікальним ідентифікатором.
    """

    queryset = Hall.objects.all()
    serializer_class = HallModelSerializer
    permission_classes = [
        IsAdminUser,
    ]
