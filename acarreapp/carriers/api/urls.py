# urls.py

from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from acarreapp.carriers.api import views as carriers_views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("carry", carriers_views.Carry)

app_name = "api_carriers"
