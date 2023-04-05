"""
Містить налаштування для адміністративного інтерфейсу.

Цей модуль містить налаштування для адміністративного інтерфейсу Django REST framework (DRF),
який надає можливість адміністрування даних через веб-інтерфейс.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

# Register your models here.
admin.site.register(User, UserAdmin)
