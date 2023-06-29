from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from acarreapp.carriers.api.urls import app_name as carriers_app_name
from acarreapp.carriers.api.urls import router as carriers_router
from acarreapp.users.api.views import UserViewSet

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
urlpatterns += [
    path("accounts/", include("dj_rest_auth.urls")),
    path("accounts/signup/", include("dj_rest_auth.registration.urls")),
    path("carriers/", include((carriers_router.urls, carriers_app_name))),
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
