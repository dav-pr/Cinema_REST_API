"""
Модуль, який визначає серіалізатори для моделей, що пов'язані з кінозалами.

Серіалізатори використовуються для перетворення складних типів даних, таких як екземпляри моделей Django,
в типи даних Python, які можна легко відобразити в формат JSON або інші типи контенту.

Цей модуль визначає серіалізатори для наступних моделей:
- CinemaModelSerializer: Серіалізатор для моделі Cinema.
- SeatModelSerializer: Серіалізатор для моделі Seat.
- HallModelSerializer: Серіалізатор для моделі Hall.
"""

from phonenumber_field.serializerfields import PhoneNumberField

from rest_framework import serializers

from cinema_hall.models import Cinema, Hall, Seat


class CinemaModelSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для моделі Cinema, який дозволяє використовувати поле PhoneNumberField для номера телефону.

    Цей серіалізатор дозволяє конвертувати об'єкти моделі Cinema в формат JSON, що використовує поля моделі.
    Додатково, для поля номеру телефону (`phone_number`) використовується спеціальний тип поля - `PhoneNumberField`,
    що дозволяє зберігати і валідувати номер телефону у форматі E.164.

    Поля моделі, що будуть серіалізовані, визначаються в параметрі `fields` класу Meta.
    Якщо `fields = "__all__"`, то будуть серіалізовані всі поля моделі Cinema.

    Приклад використання:
    serializer = CinemaModelSerializer(instance=cinema)
    serialized_data = serializer.data
    """

    phone_number = PhoneNumberField()

    class Meta:
        """
        Клас Meta для серіалізатора моделі Cinema.

        Цей клас містить метадані для серіалізатора моделі Cinema. У даному випадку, використовується модель `Cinema`.
        Параметр `fields` визначає, які поля моделі будуть серіалізовані. Якщо `fields = "__all__"`, то будуть
        серіалізовані всі поля моделі. Інакше, `fields` повинен містити список полів, які потрібно серіалізувати.
        """

        model = Cinema
        fields = "__all__"


class SeatModelSerializer(serializers.ModelSerializer):
    """
    Клас SeatModelSerializer є серіалізатором Django.

    Клас SeatModelSerializer є серіалізатором Django, який використовується для перетворення об'єктів моделі Seat
    на JSON-об'єкти та навпаки.
    Атрибут Meta цього класу містить метадані, необхідні для правильного виконання серіалізації та десеріалізації
    об'єктів моделі Seat. В даному випадку, вказано, що модель, яку необхідно серіалізувати, - це Seat, та вказано,
    які саме поля моделі повинні бути серіалізовані у JSON-об'єкт.
    Конкретно, цей серіалізатор серіалізує три поля моделі Seat: id, row та number. Для цього використовується клас
    ModelSerializer з бібліотеки rest_framework.serializers.
    """

    class Meta:
        """
        Клас Meta для серіалізатора моделі Seat.

        Цей клас містить метадані для серіалізатора моделі Seat.
        """

        model = Seat
        fields = (
            "id",
            "row",
            "number",
        )


class HallModelSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для моделі Hall з використанням серіалізатора моделі Seat.

    Цей серіалізатор дозволяє конвертувати об'єкти моделі Hall в формат JSON, що використовує поля моделі.
    Для поля `seats` використовується серіалізатор моделі `SeatModelSerializer` з параметрами `many=True` та
    `read_only=True`, що дозволяє серіалізувати багато екземплярів моделі `Seat` та забороняє їх зміну через API.
    Для поля `seats_tuple` використовується тип поля `ListField` з параметром `child=serializers.IntegerField()`, що
    дозволяє передавати тільки список цілих чисел.

    Поля моделі, що будуть серіалізовані, визначаються в параметрі `fields` класу Meta.
    """

    seats = SeatModelSerializer(
        many=True,
        read_only=True,
    )
    seats_tuple = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
    )

    class Meta:
        """
        Клас Meta для серіалізатора моделі Hall.

        Цей клас містить метадані для серіалізатора моделі Hall. У даному випадку, використовується модель `Hall`.
        Параметр `fields` визначає, які поля моделі будуть серіалізовані. Якщо потрібно серіалізувати всі поля, то
        використовується `fields = "__all__"`. Інакше, `fields` повинен містити список полів, які потрібно
        серіалізувати.
        """

        model = Hall
        fields = (
            "id",
            "name",
            "cinema",
            "seats",
            "seats_tuple",
        )

    def create(self, validated_data):
        """
        Метод `create` для серіалізатора моделі `Hall`.

        Цей метод створює новий об'єкт моделі `Hall` на основі переданих даних у параметрі `validated_data`.
        Дані в цьому параметрі уже пройшли валідацію.

        Метод перетворює список `validated_data["seats_tuple"]`, що містить кількість місць в кожному ряду залу,
        на список екземплярів моделі `Seat`, які будуть пов'язані з новоствореним залом. Для цього використовується
        функція `bulk_create`, яка ефективно створює багато об'єктів одним запитом до бази даних.

        Параметри:
        - validated_data (dict): словник з валідованими даними для створення нового залу.

        Повертає:
        - hall (Hall): екземпляр новоствореного залу.
        """
        hall = Hall.objects.create(
            cinema=validated_data["cinema"],
            name=validated_data["name"],
        )
        seats = []
        for row, seats_count in enumerate(
            validated_data["seats_tuple"],
            start=1,
        ):
            seats.extend(
                [
                    Seat(
                        hall=hall,
                        row=row,
                        number=number,
                    )
                    for number in range(
                        1,
                        seats_count + 1,
                    )
                ]
            )
        Seat.objects.bulk_create(seats)
        """
        bulk_create є методом Django ORM, який дозволяє ефективно створити багато екземплярів моделі одним запитом до
        бази даних. Це корисний метод, якщо ми хочемо створити багато записів у базі даних, наприклад, коли потрібно
        створити багато об'єктів моделі зразу після створення батьківського об'єкта.
        У випадку з Seat.objects.bulk_create(seats), ми передаємо список екземплярів моделі Seat, які ми хочемо
        створити, як параметр методу bulk_create. Django створює один запит до бази даних для вставки усіх елементів
        списку seats в таблицю бази даних, яка відповідає моделі Seat.
        Це ефективний спосіб створення багатьох записів у базі даних одним запитом замість того, щоб створювати кожний
        запис окремо і робити окремий запит до бази даних для кожного запису, що може призвести до більшої кількості
        запитів та сповільнення роботи програми."""

        return hall
