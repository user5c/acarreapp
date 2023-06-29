from django.contrib import admin

from acarreapp.carriers import models as carriers_models


@admin.register(carriers_models.Carrier)
class Carrier(admin.ModelAdmin):
    list_display = [
        "id",
        "lat_now",
        "long_now",
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


@admin.register(carriers_models.Carry)
class Carry(admin.ModelAdmin):
    list_display = [
        "id",
        "carrier",
        "client",
        "payment_type",
        "status",
        "check_in_time",
        "check_out_time",
    ]


@admin.register(carriers_models.Client)
class Client(admin.ModelAdmin):
    list_display = [
        "user",
        "photo",
        "doc_type",
        "doc_number",
    ]


@admin.register(carriers_models.Load)
class Load(admin.ModelAdmin):
    list_display = [
        "id",
        "carry",
        "furniture_type",
        "furniture_quantity",
        "help_required",
        "furniture_load",
        "furniture_weight_kg",
        "furniture_weight_m3",
        "furniture_photo",
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
