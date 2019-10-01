# Generated by Django 2.2.5 on 2019-09-27 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("ticketing", "0010_customuser_u_sort_type")]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="u_sort_type",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="Sort By Value"
            ),
        )
    ]
