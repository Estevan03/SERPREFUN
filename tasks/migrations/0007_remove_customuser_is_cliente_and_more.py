# Generated by Django 4.2.6 on 2023-11-26 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_customuser_is_empleado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_cliente',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='is_empleado',
        ),
    ]