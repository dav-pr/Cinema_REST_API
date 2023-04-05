"""
Цей модуль admin.py містить налаштування адміністративної частини додатку screening.

Він містить класи Movie, що надають можливість керувати моделями
бази даних через веб-інтерфейс Django.
"""
from django.contrib import admin

from cinema.admin import AdminInteractPermissionModelAdminMixin
from screening.models import Movie


"""
Цей код реєструє модель Movie в адміністративному інтерфейсі Django за допомогою декоратора admin.site.register() і
додає до неї клас AdminInteractPermissionModelAdminMixin в якості mixin-класу.
Mixin-класи є одним із способів додавання функціональності до класів в Python.
У цьому випадку AdminInteractPermissionModelAdminMixin додає до адміністративного інтерфейсу Django функціональність,
що вимагає від користувачів певних дозволів для редагування та видалення об'єктів моделі Movie.
"""
admin.site.register(
    Movie,
    AdminInteractPermissionModelAdminMixin,
)
