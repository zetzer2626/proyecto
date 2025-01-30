# Generated by Django 5.1.2 on 2025-01-23 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_proyecto_link_2_remove_proyecto_link_3_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='nombre_enlace_2',
        ),
        migrations.RemoveField(
            model_name='proyecto',
            name='nombre_enlace_3',
        ),
        migrations.RemoveField(
            model_name='proyecto',
            name='nombre_enlace_4',
        ),
        migrations.RemoveField(
            model_name='proyecto',
            name='nombre_enlace_5',
        ),
        migrations.AlterField(
            model_name='boleta',
            name='año',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='boleta',
            name='monto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='boleta',
            name='nombre',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='boleta',
            name='numero_cheque',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='boleta',
            name='numero_talonario',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='boleta',
            name='presupuesto',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
