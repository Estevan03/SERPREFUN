# Generated by Django 4.2.6 on 2023-12-10 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0015_pedidoproducto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='servicio',
        ),
        migrations.AddField(
            model_name='pedido',
            name='servicios',
            field=models.ManyToManyField(blank=True, to='tasks.service'),
        ),
    ]
