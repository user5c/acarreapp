import hashlib
import uuid

from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Carrier(TimestampedModel):
    def photo_path(self, filename):
        key = Fernet.generate_key()
        index_of_dot = filename.rfind(".")
        extension = filename[index_of_dot:]
        md5_id = hashlib.md5(settings.MEDIA_URL_PUBLIC.encode()).hexdigest()
        return f"{md5_id}/_{key.decode()[:-1]}_{extension}"

    def license_file_path(self, filename):
        key = Fernet.generate_key()
        index_of_dot = filename.rfind(".")
        extension = filename[index_of_dot:]
        md5_id = hashlib.md5(settings.MEDIA_URL_PUBLIC.encode()).hexdigest()
        return f"{md5_id}/_{key.decode()[:-1]}_{extension}"

    class DocType(models.TextChoices):
        CC = "CC", "Cedula de ciudadanía"
        PASSPORT = "PST", "Pasaporte"

    class LicenseType(models.TextChoices):
        # doc: https://www.autofact.com.co/blog/mi-carro/conduccion/tipos-de-licencia
        A1 = "A1", "Licencia Clase A1"
        A2 = "A2", "Licencia Clase A2"
        B1 = "B1", "Licencia Clase B1"
        B2 = "B2", "Licencia Clase B2"
        B3 = "B3", "Licencia Clase B3"
        C1 = "C1", "Licencia Clase C1"
        C2 = "C2", "Licencia Clase C2"
        C3 = "C3", "Licencia Clase C3"

    user = models.OneToOneField(User, models.CASCADE)
    photo = models.ImageField(upload_to=photo_path)
    doc_type = models.CharField(max_length=20, choices=DocType.choices)
    doc_number = models.IntegerField()
    vehicle = models.ForeignKey("Vehicle", models.SET_NULL, null=True)
    license_number = models.CharField(max_length=50)
    license_type = models.CharField(max_length=17, choices=LicenseType.choices)
    license_due_date = models.DateField()
    license_file = models.FileField(upload_to=license_file_path)


class Carry(TimestampedModel):
    class PaymentType(models.TextChoices):
        BANK_TRANSFER = "BT", "Bank Transfer"
        CASH = "CA", "Cash"

    class StatusChoices(models.TextChoices):
        CREATED = "created", "Created"
        ACCEPTED = "accepted", "Accepted"
        CANCELED_BY_USER = "canceled", "Canceled by User"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carrier = models.ForeignKey(Carrier, models.CASCADE, null=True, blank=True)
    client = models.ForeignKey("Client", models.CASCADE, null=True, blank=True)
    lat_from = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long_from = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lat_to = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long_to = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    payment_type = models.CharField(max_length=10, choices=PaymentType.choices, null=True, blank=True)
    price_offered_by_client = models.IntegerField(default=0)
    price_offered_by_carrier = models.IntegerField(default=0)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.CREATED)


class Client(TimestampedModel):
    def photo_path(self, filename):
        key = Fernet.generate_key()
        index_of_dot = filename.rfind(".")
        extension = filename[index_of_dot:]
        md5_id = hashlib.md5(str(self.user.pk).encode()).hexdigest()
        return f"{md5_id}/_{key.decode()[:-1]}_{extension}"

    class DocType(models.TextChoices):
        CC = "CC", "Cedula de ciudadanía"
        PASSPORT = "PST", "Pasaporte"

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    photo = models.ImageField(upload_to=photo_path)
    doc_type = models.CharField(max_length=20, choices=DocType.choices)
    doc_number = models.IntegerField()


class Load(models.Model):
    def furniture_photo_path(self, filename):
        key = Fernet.generate_key()
        index_of_dot = filename.rfind(".")
        extension = filename[index_of_dot:]
        md5_id = hashlib.md5(settings.MEDIA_URL_PUBLIC.encode()).hexdigest()
        return f"{md5_id}/_{key.decode()[:-1]}_{extension}"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    carry = models.ForeignKey(Carry, on_delete=models.CASCADE)
    furniture_type = models.CharField(max_length=255)
    furniture_quantity = models.IntegerField()
    help_required = models.BooleanField(default=False)
    furniture_load = models.BooleanField(default=False)
    furniture_weight_kg = models.FloatField()
    furniture_weight_m3 = models.FloatField()
    furniture_photo = models.ImageField(upload_to=furniture_photo_path)


class Vehicle(models.Model):
    def image_path(self, filename):
        key = Fernet.generate_key()
        index_of_dot = filename.rfind(".")
        extension = filename[index_of_dot:]
        md5_id = hashlib.md5(settings.MEDIA_URL_PUBLIC.encode()).hexdigest()
        return f"{md5_id}/_{key.decode()[:-1]}_{extension}"

    class Type(models.TextChoices):
        CAMIONETA = "camioneta"
        FURGON = "furgon"
        CAMION = "camion"

    type = models.CharField(max_length=9, choices=Type.choices)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=40)
    year = models.SmallIntegerField()
    image = models.ImageField(upload_to=image_path)
