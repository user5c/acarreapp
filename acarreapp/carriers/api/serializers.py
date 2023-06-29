from django.contrib.auth import get_user_model
from rest_framework import serializers

from acarreapp.carriers import models as carriers_models
from acarreapp.carriers.utils import carry as utils_carry

# from django.contrib.gis.db import models as gis_models


User = get_user_model()


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

        class User(serializers.ModelSerializer):
            class Meta:
                model = User
                fields = ["id", "name", "username", "email"]

        vehicle = Vehicle()
        user = User()

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

    def update(self, instance, validated_data):
        # 1. Obtener Client para colocarlo en la Carrera
        user_obj = self.context["request"].user
        client_obj = carriers_models.Client.objects.get(user=user_obj)
        validated_data["client"] = client_obj

        # 2. Cambiar de estado a la carrera a ACCEPTED
        validated_data["status"] = carriers_models.Carry.StatusChoices.ACCEPTED

        # 3. Calcular numero de kilometros
        validated_data["price_offered_by_client"] = utils_carry.calculate_price(
            carry_obj=instance,
            lat_from=validated_data["lat_from"],
            long_from=validated_data["long_from"],
            lat_to=validated_data["lat_to"],
            long_to=validated_data["long_to"],
        )

        return super().update(instance, validated_data)
