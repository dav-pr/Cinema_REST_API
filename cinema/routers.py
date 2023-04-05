"""
Модуль routers.py містить налаштування маршрутизаторів для додатку Django.

Маршрутизатори дозволяють визначити, які моделі повинні використовувати певні джерела даних
(наприклад, базу даних або зовнішні API) в залежності від потреб додатку.
Це дає можливість ефективно керувати даними та зменшувати навантаження на базу даних.
Модуль містить класи, які визначають маршрутизацію для різних моделей додатку.
Ці класи повинні бути зареєстровані в налаштуваннях додатку Django для використання.
Цей модуль є частиною додатку та повинен бути встановлений та налаштований разом з ним.
"""

from cinema_hall import views as cinema_hall_views

from purchase import views as purchase_views

from rest_framework.routers import DefaultRouter

from screening import views as screening_views

from users import views as users_views

router = DefaultRouter()
"""
DefaultRouter є класом, що належить модулю rest_framework.routers бібліотеки Django REST framework.
Він створює маршрутизатор з дефолтними методами для REST API, такими як GET, POST, PUT, PATCH, DELETE.
DefaultRouter дозволяє з легкістю створити маршрути для всіх CRUD-операцій (Create, Retrieve, Update, Delete)
для різних ресурсів API, прив'язавши їх до відповідних в'юх. Для цього потрібно лише зареєструвати відповідні
в'юхи з використанням методів, які відповідають кожному з дозволених методів HTTP.
DefaultRouter також дозволяє генерувати URL-шляхи для зазначених ресурсів, що вказані в методі register()
з класу ViewSet. Наприклад, при реєстрації в'юхи для ресурсу users можна автоматично
згенерувати URL-шляхи /users/ та /users/<pk>/, які відповідатимуть методам GET та PUT/PATCH/DELETE відповідно.
Узагальнюючи, DefaultRouter є потужним інструментом для автоматизації створення REST API в Django,
що дозволяє швидко налаштувати маршрути та в'юхи для різних ресурсів.
"""

router.register(
    "cinema",
    cinema_hall_views.CinemaViewSet,
    basename="cinema",
)
"""
router.register() - це метод класу DefaultRouter з бібліотеки Django REST framework, який використовується для
реєстрації в'юх (viewset) для маршрутів API.
Перший параметр cinema є шляхом маршруту, який відображається у URL-адресі API.
Другий параметр cinema_hall_views.CinemaViewSet є класом в'юх, який відповідає за обробку запитів до маршруту cinema.
Останній параметр basename встановлює префікс для генерації імені маршруту.
Клас CinemaViewSet може бути будь-яким класом в'юх, який успадковується від базового класу ViewSet.
У такому класі визначаються методи list(), create(), retrieve(), update(), partial_update() та destroy(),
які відповідають відповідним методам HTTP-запитів GET, POST, GET, PUT, PATCH та DELETE відповідно.
В'юха, зазвичай, працює з даними моделі, пов'язаної з даним маршрутом.
У разі реєстрації в'юхи з router.register(), DefaultRouter автоматично генерує маршрути для всіх методів HTTP-запитів,
що відповідають класу в'юх. У цьому конкретному випадку будуть зареєстровані маршрути для методів GET, POST, PUT,
PATCH, DELETE з шляхом /cinema/ та /cinema/<id>/, де <id> - ідентифікатор об'єкту, з яким працює в'юха.
Ці маршрути дозволяють виконувати всі необхідні операції з об'єктами моделі, яка пов'язана з цим маршрутом.
"""

router.register(
    "hall",
    cinema_hall_views.HallViewSet,
    basename="hall",
)
router.register(
    "movie",
    screening_views.MovieViewSet,
    basename="movie",
)
router.register(
    "screening_session",
    screening_views.ScreeningSessionViewSet,
    basename="screening_session",
)
router.register(
    "screening",
    screening_views.ScreeningViewSet,
    basename="screening",
)
router.register(
    "order",
    purchase_views.OrderViewSet,
    basename="order",
)
router.register(
    "users",
    users_views.UserViewSet,
    basename="users",
)

urlpatterns = router.urls
"""
urlpatterns вказує Django, як обробляти HTTP-запити до нашого API. Окрім того, у список urlpatterns можна додавати
інші URL-адреси, наприклад, для статичного контенту або інших додатків.
"""
