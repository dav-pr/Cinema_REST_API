"""Модуль serializers містить клас UserModelSerializer для серіалізації та десеріалізації об'єктів моделі користувача.

Класи:
- UserModelSerializer: ModelSerializer для серіалізації та десеріалізації об'єктів моделі користувача з кодованим
паролем.
"""


from django.contrib.auth import get_user_model

from rest_framework import serializers

UserModel = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    """Serializer для моделі користувача.

    Serializer містить поля, які можна відобразити, а також поля, які можна лише записати або лише читати.
    Крім того, він містить функцію створення користувача на основі переданих даних.

    Атрибути:
    - model: модель користувача, яку буде використовувати Serializer.
    - fields: перелік полів моделі користувача, які будуть відображені.
    - write_only_fields: перелік полів моделі користувача, які можна лише записати (наприклад, пароль).
    - read_only_fields: перелік полів моделі користувача, які можна лише читати (наприклад, ідентифікатор

    та баланс користувача).

    Методи:
    - create(validated_data): створення нового користувача на основі переданих даних. Пароль кодується перед
    збереженням у базі даних.
    """

    class Meta:
        """Клас налаштувань Serializer для моделі користувача.

        Атрибути:
        - model: модель користувача, яку буде використовувати Serializer.
        - fields: перелік полів моделі користувача, які будуть відображені в серіалізованому представленні.
        - write_only_fields: перелік полів моделі користувача, які можна лише записати та які не будуть відображатися
        в серіалізованому представленні (наприклад, пароль).
        - read_only_fields: перелік полів моделі користувача, які можна лише читати та які будуть відображатися в
        серіалізованому представленні (наприклад, ідентифікатор та баланс користувача).
        """

        model = UserModel
        fields = ("id", "username", "password", "email", "first_name", "last_name", "balance")
        write_only_fields = ("password", )
        read_only_fields = ("id", "balance")

    def create(self, validated_data):
        """Створення нового користувача.

        Метод створює нового користувача на основі переданих даних та зберігає його в базі даних.
        Пароль кодується перед збереженням.
        Аргументи:
        - validated_data: словник з перевіреними та очищеними даними користувача.
        Повертає:
        - user: створений об'єкт користувача.
        """
        user = UserModel.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user
