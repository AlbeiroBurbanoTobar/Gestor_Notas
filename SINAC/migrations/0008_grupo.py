# Generated by Django 5.1.6 on 2025-03-05 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SINAC", "0007_asignatura"),
    ]

    operations = [
        migrations.CreateModel(
            name="Grupo",
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
                ("nombre", models.CharField(max_length=100, unique=True)),
                (
                    "nivel",
                    models.IntegerField(
                        choices=[
                            (1, "1"),
                            (2, "2"),
                            (3, "3"),
                            (4, "4"),
                            (5, "5"),
                            (6, "6"),
                            (7, "7"),
                            (8, "8"),
                            (9, "9"),
                            (10, "10"),
                            (11, "11"),
                        ]
                    ),
                ),
            ],
        ),
    ]
