# Generated by Django 2.2.5 on 2019-09-25 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("ticketing", "0008_auto_20190925_1312")]

    operations = [
        migrations.DeleteModel(name="Customer"),
        migrations.DeleteModel(name="Technician"),
    ]
