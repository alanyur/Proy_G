# Generated by Django 5.2.3 on 2025-07-05 18:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_servicio_usuario_rol_disponibilidad_solicitud_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disponibilidad',
            name='trabajador',
            field=models.ForeignKey(limit_choices_to={'rol': 'trabajador'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
