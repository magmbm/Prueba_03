# Generated by Django 5.0.6 on 2024-07-03 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0009_alter_game_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="id",
            field=models.IntegerField(
                db_column="game_id", primary_key=True, serialize=False
            ),
        ),
    ]
