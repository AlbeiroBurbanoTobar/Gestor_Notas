# Generated by Django 5.1.6 on 2025-03-05 22:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("SINAC", "0008_grupo"),
    ]

    operations = [
        migrations.AddField(
            model_name="estudiante",
            name="grupo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="SINAC.grupo",
            ),
        ),
    ]
