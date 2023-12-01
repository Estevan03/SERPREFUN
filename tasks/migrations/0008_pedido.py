# Generated by Django 4.2.6 on 2023-12-01 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0007_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=255)),
                ('tipo_documento', models.CharField(max_length=50)),
                ('numero_documento', models.CharField(max_length=50)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('numero_celular', models.CharField(max_length=20)),
                ('direccion', models.TextField()),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.service')),
            ],
        ),
    ]
