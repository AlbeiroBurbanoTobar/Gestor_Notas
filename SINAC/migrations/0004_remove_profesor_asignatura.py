# Generated by Django 5.1.6 on 2025-03-05 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("SINAC", "0003_alter_usuario_rol"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profesor",
            name="asignatura",
        ),
    ]
