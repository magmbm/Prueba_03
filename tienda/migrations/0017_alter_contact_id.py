# Generated by Django 5.0.6 on 2024-07-09 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0016_game_valoracion"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]