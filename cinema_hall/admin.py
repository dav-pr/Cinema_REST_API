"""
Цей модуль admin.py містить налаштування адміністративної частини додатку cinema_hall.

Він реєструє  класи Cinema та AdminInteractPermissionModelAdminMixin, що надають можливість керувати моделями
бази даних через веб-інтерфейс Django.
"""

from django.contrib import admin

from cinema.admin import AdminInteractPermissionModelAdminMixin

from cinema_hall.models import Cinema, Hall, Seat

admin.site.register(
    Cinema,
    AdminInteractPermissionModelAdminMixin,
)

admin.site.register(
    Hall,
    AdminInteractPermissionModelAdminMixin,
)

admin.site.register(
    Seat,
    AdminInteractPermissionModelAdminMixin,
)