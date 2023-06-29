from rest_framework import serializers

from acarreapp.carriers import models as carriers_models


class Carry(serializers.ModelSerializer):
    class Carrier(serializers.ModelSerializer):
        class Vehicle(serializers.ModelSerializer):
            class Meta:
                model = carriers_models.Vehicle
                fields = [
                    # 'id',
                    "type",
                    "brand",
                    "model",
                    "color",
                    # 'year',
                    "image",
                ]

        vehicle = Vehicle()

        class Meta:
            model = carriers_models.Carrier
            fields = (
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
                "lat_now",
                "long_now",
            )

    class Client(serializers.ModelSerializer):
        photo = serializers.ImageField(required=True)

        class Meta:
            model = carriers_models.Client
            fields = ["user", "photo", "doc_type", "doc_number"]

    class Load(serializers.ModelSerializer):
        class Meta:
            model = carriers_models.Load
            fields = (
                "id",
                "carry",
                "furniture_type",
                "furniture_quantity",
                "help_required",
                "furniture_load",
                "furniture_weight_kg",
                "furniture_weight_m3",
                "furniture_photo",
            )

    carrier = Carrier()
    client = Client()

    load_set = Load(many=True, read_only=True)

    class Meta:
        model = carriers_models.Carry
        fields = [
            "id",
            "carrier",
            "client",
            "lat_from",
            "long_from",
            "lat_to",
            "long_to",
            "payment_type",
            "price_offered_by_client",
            "price_offered_by_carrier",
            "check_in_time",
            "check_out_time",
            "status",
            "load_set",
        ]
