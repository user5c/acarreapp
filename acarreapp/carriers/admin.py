from django.contrib import admin

from acarreapp.carriers import models as carriers_models


@admin.register(carriers_models.Carrier)
class Carrier(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "photo",
        "doc_type",
        "doc_number",
        "vehicle",
        "license_number",
        "license_type",
        "license_due_date",
        "license_file",
    ]


@admin.register(carriers_models.Vehicle)
class Vehicle(admin.ModelAdmin):
    list_display = [
        "id",
        "type",
        "brand",
        "model",
        "color",
        "year",
        "image",
    ]
