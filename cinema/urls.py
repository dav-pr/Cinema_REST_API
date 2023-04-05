"""cinema URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from cinema.routers import urlpatterns as router_urlpatterns

"""
drf_spectacular - це пакет для Django REST framework, який дозволяє автоматично генерувати документацію для вашого API.
SpectacularAPIView - це в'ю для генерації специфікації OpenAPI, яка включає опис всіх маршрутів API та іншої
мета-інформації. Цю в'ю можна використовувати, щоб отримати специфікацію у форматі JSON або YAML.
SpectacularRedocView - це в'ю, яка генерує інтерактивну документацію у форматі ReDoc.
ReDoc - це спеціальний інструмент, який дозволяє візуалізувати специфікацію OpenAPI у вигляді зручної для
користувача документації зі згортанням секцій та можливістю пошуку.
SpectacularSwaggerView - це в'ю, яка генерує інтерактивну документацію у форматі Swagger UI.
Swagger UI - це інструмент, який дозволяє візуалізувати специфікацію OpenAPI у вигляді інтерактивної документації
з можливістю тестування API напряму з веб-інтерфейсу.
Ці в'ю можна додати до вашого проекту Django REST framework, щоб забезпечити легкий доступ до документації вашого API.
Використання drf_spectacular дозволяє зменшити ручну роботу з написанням документації та підтримкою її у відповідності
до специфікації OpenAPI.
"""

"""
rest_framework_simplejwt - це пакет для Django REST framework, який дозволяє додавати підтримку JWT-аутентифікації
до вашого API.
TokenObtainPairView - це в'ю, яка дозволяє створювати пару токенів (access token та refresh token) для аутентифікації
користувача. Клієнт повинен використовувати access token для авторизації запитів до захищених ресурсів,
а refresh token - для отримання нової пари токенів після закінчення терміну дії старої пари.
TokenRefreshView - це в'ю, яка дозволяє оновлювати пару токенів (access token та refresh token) за допомогою
refresh token. Ця в'ю поверне нову пару токенів, які можна використовувати для подальшої авторизації.
TokenVerifyView - це в'ю, яка дозволяє перевіряти чинність токенів. Клієнт може відправити access token до цієї в'ю,
щоб перевірити, чи дійсний токен, та отримати інформацію про користувача, який видавав токен.
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/",
        include(router_urlpatterns),
    ),
    # auth
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
    # Docs
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema",
        ),
        name="redoc",
    ),
]
