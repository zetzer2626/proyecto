# Generated by Django 5.1.2 on 2025-02-18 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_remove_proyecto_nombre_enlace_2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='enlace_documento',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]
