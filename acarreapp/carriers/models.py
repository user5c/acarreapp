import hashlib

from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Carrier(models.Model):
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
        CC = "Cedula de ciudadanía"
        PASSPORT = "Pasaporte"

    class LicenseType(models.TextChoices):
        # doc: https://www.autofact.com.co/blog/mi-carro/conduccion/tipos-de-licencia
        A1 = "Licencia Clase A1"
        A2 = "Licencia Clase A2"
        B1 = "Licencia Clase B1"
        B2 = "Licencia Clase B2"
        B3 = "Licencia Clase B3"
        C1 = "Licencia Clase C1"
        C2 = "Licencia Clase C2"
        C3 = "Licencia Clase C3"

    user = models.OneToOneField(User, models.CASCADE)
    photo = models.ImageField(upload_to=photo_path)
    doc_type = models.CharField(max_length=20, choices=DocType.choices)
    doc_number = models.IntegerField()
    vehicle = models.ForeignKey("Vehicle", models.SET_NULL, null=True)
    license_number = models.CharField(max_length=50)
    license_type = models.CharField(max_length=17, choices=LicenseType.choices)
    license_due_date = models.DateField()
    license_file = models.FileField(upload_to=license_file_path)


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
