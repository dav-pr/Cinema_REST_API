from rest_framework.routers import DefaultRouter

from cinema_hall import views as cinema_hall_views
from purchase import views as purchase_views
from screening import views as screening_views
from users import views as users_views

router = DefaultRouter()

router.register(
    "cinema",
    cinema_hall_views.CinemaViewSet,
    basename="cinema",
)
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
