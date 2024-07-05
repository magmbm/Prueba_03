# Generated by Django 5.0.6 on 2024-07-03 17:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0005_alter_cliente_telefono"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pedido",
            name="f_producto",
        ),
        migrations.RemoveField(
            model_name="pedido",
            name="valor_total",
        ),
        migrations.AddField(
            model_name="game",
            name="imagen",
            field=models.CharField(
                default="https://github.com/magmbm/SQL_img/blob/main/control-del-juego.png",
                max_length=1000,
            ),
        ),
        migrations.AddField(
            model_name="pedido",
            name="current",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="pedido",
            name="fecha_compra",
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name="Record",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cant", models.IntegerField()),
                ("precio", models.IntegerField()),
                (
                    "f_game",
                    models.ForeignKey(
                        db_column="game_FK",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tienda.game",
                    ),
                ),
                (
                    "pedido_FK",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tienda.pedido"
                    ),
                ),
            ],
        ),
    ]