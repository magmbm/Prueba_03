# Generated by Django 5.0.6 on 2024-07-01 20:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0002_cliente_user_alter_cliente_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cliente",
            name="rut",
        ),
    ]
