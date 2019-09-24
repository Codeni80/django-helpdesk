# Generated by Django 2.2.5 on 2019-09-24 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=100, verbose_name='Password'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='u_permission_level',
            field=models.CharField(choices=[('1', 'User'), ('2', 'Technician')], max_length=11, verbose_name='Permission Level'),
        ),
    ]
