# Generated by Django 4.1.9 on 2023-06-29 03:42

import acarreapp.carriers.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("carriers", "0004_alter_carry_carrier_alter_carry_check_in_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="client",
            name="phone",
            field=models.CharField(default=3159090011, max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="client",
            name="photo",
            field=models.ImageField(null=True, upload_to=acarreapp.carriers.models.Client.photo_path),
        ),
    ]