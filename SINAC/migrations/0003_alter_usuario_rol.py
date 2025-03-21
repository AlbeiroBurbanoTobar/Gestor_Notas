# Generated by Django 5.1.6 on 2025-03-05 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SINAC", "0002_remove_estudiante_curso_profesor_documento"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="rol",
            field=models.CharField(
                choices=[
                    ("ADMINISTRADOR", "Administrador"),
                    ("ESTUDIANTE", "Estudiante"),
                    ("PROFESOR", "PROFESOR"),
                ],
                default="ESTUDIANTE",
                max_length=20,
            ),
        ),
    ]
