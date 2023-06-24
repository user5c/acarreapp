from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CarriersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "acarreapp.carriers"
    verbose_name = _("Carriers")
