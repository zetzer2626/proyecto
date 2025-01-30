# Generated by Django 5.1.2 on 2025-01-22 16:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presupuesto', models.CharField(max_length=5)),
                ('nombre', models.CharField(max_length=200)),
                ('monto', models.IntegerField(blank=True, null=True)),
                ('correspondiente', models.TextField(blank=True, max_length=1000, null=True)),
                ('fecha', models.CharField(blank=True, max_length=200, null=True)),
                ('forma_pago', models.CharField(blank=True, choices=[('efectivo', 'Efectivo'), ('transferencia', 'Transferencia'), ('tarjeta', 'Tarjeta')], max_length=100, null=True)),
                ('recibido', models.CharField(blank=True, max_length=200, null=True)),
                ('firma', models.CharField(blank=True, max_length=200, null=True)),
                ('rut', models.CharField(blank=True, max_length=30, null=True)),
                ('numero_talonario', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
            ],
        ),
        migrations.CreateModel(
            name='Contactos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('CLIENTE', 'Cliente'), ('CLIENTE PROYECTO', 'Cliente Proyecto'), ('CLIENTE LOTE', 'Cliente Lote'), ('PROFESIONAL', 'Profesional'), ('ENTIDAD', 'Entidad'), ('OTROS', 'Otros')], max_length=20)),
                ('telefono', models.CharField(max_length=15)),
                ('correo', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Enlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=5000, null=True)),
                ('link', models.URLField(blank=True, max_length=500, null=True)),
                ('documento_pdf', models.FileField(blank=True, null=True, upload_to='pdf/')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
            ],
        ),
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('completado', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Insumos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solicitante', models.CharField(blank=True, max_length=100, null=True)),
                ('descripcion', models.TextField()),
                ('fecha_solicitud', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha_recepcion', models.CharField(blank=True, max_length=200, null=True)),
                ('pago', models.FileField(blank=True, null=True, upload_to='insumos/')),
                ('factura', models.FileField(blank=True, null=True, upload_to='insumos/')),
                ('valor_total', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Listado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presupuesto', models.CharField(blank=True, max_length=100, null=True)),
                ('año', models.CharField(blank=True, max_length=10, null=True)),
                ('nombre', models.CharField(blank=True, max_length=200, null=True)),
                ('gestion', models.TextField()),
                ('nota', models.TextField()),
                ('listado', models.URLField(blank=True, max_length=500, null=True)),
                ('drive', models.URLField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pago_tramitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_pago', models.CharField(choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso')], default='ingreso', max_length=10)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('origen', models.CharField(blank=True, max_length=100, null=True)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('gestion', models.TextField()),
                ('ingreso', models.IntegerField(blank=True, null=True)),
                ('egreso', models.IntegerField(blank=True, null=True)),
                ('transferencia', models.FileField(blank=True, null=True, upload_to='pago_tramitaciones/')),
                ('boletabyd', models.FileField(blank=True, null=True, upload_to='pago_tramitaciones/')),
                ('facturabyd', models.FileField(blank=True, null=True, upload_to='pago_tramitaciones/')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('presupuesto', models.CharField(max_length=200)),
                ('nombre', models.CharField(max_length=200)),
                ('telefono', models.CharField(blank=True, max_length=255, null=True)),
                ('correo', models.CharField(blank=True, max_length=255, null=True)),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('rol_avaluo', models.CharField(blank=True, max_length=100, null=True)),
                ('año', models.IntegerField(blank=True, null=True)),
                ('proyecto', models.CharField(blank=True, max_length=255, null=True)),
                ('estado_proyecto', models.CharField(blank=True, choices=[('no_concretado', 'No Concretado'), ('trabajando', 'Trabajar en Proyecto'), ('ingreso_dom', 'Ingresado DOM'), ('ingresado_sag', 'Ingresado SAG'), ('ingresado_minvu', 'Ingresado Minvu'), ('ingresado_monumento', 'Ingresado Monumento'), ('observado', 'Ingresado Observado'), ('rechazado', 'Ingresado Rechazado'), ('aprobado', 'Aprobado'), ('realizado', 'Realizado'), ('congelado', 'Congelado')], max_length=50, null=True)),
                ('detalle', models.TextField(blank=True, max_length=10000, null=True)),
                ('descripcion', models.TextField(blank=True, max_length=10000, null=True)),
                ('kardex', models.CharField(blank=True, max_length=255, null=True)),
                ('proceso', models.CharField(blank=True, choices=[('terminado', 'Terminado'), ('No Aplica', 'No Aplica'), ('pendiente', 'Pendiente')], max_length=20, null=True)),
                ('levantamiento', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('escritura', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('dominio_vigente', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('cedula_identidad', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('poder', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('boleta_agua', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('boleta_luz', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('rol_avaluo_detallado', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('proyecto_anterior', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('conjunto_habitacional', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('informe_previo', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('utilidad_publica', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('certificado_numero', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('factibilidad', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('seim', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('listado', models.FileField(blank=True, null=True, upload_to='documentos/')),
                ('opcional_1', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('opcional_2', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('opcional_3', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('opcional_4', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('opcional_5', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('opcional_6', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('opcional_7', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('opcional_8', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('opcional_9', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('opcional_10', models.FileField(blank=True, null=True, upload_to='opcional/')),
                ('link_1', models.URLField(blank=True, max_length=500, null=True)),
                ('link_2', models.URLField(blank=True, max_length=500, null=True)),
                ('link_3', models.URLField(blank=True, max_length=500, null=True)),
                ('link_4', models.URLField(blank=True, max_length=500, null=True)),
                ('link_5', models.URLField(blank=True, max_length=500, null=True)),
                ('nombre_enlace_1', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_enlace_2', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_enlace_3', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_enlace_4', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_enlace_5', models.CharField(blank=True, max_length=255, null=True)),
                ('documento_presupuesto_1', models.FileField(blank=True, null=True, upload_to='presupuesto/')),
                ('documento_presupuesto_2', models.FileField(blank=True, null=True, upload_to='presupuesto/')),
                ('presupuesto_link', models.URLField(blank=True, max_length=500, null=True)),
                ('nombre_ingreso_1', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_ingreso_2', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_ingreso_3', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_ingreso_4', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_ingreso_5', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_ingreso_6', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_ingreso_7', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_ingreso_8', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_ingreso_9', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre_ingreso_10', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solicitante', models.CharField(max_length=200)),
                ('nombre_documento', models.CharField(max_length=200)),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha_solicitud', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha_recepcion', models.CharField(blank=True, max_length=200, null=True)),
                ('descripcion', models.TextField(blank=True, max_length=10000, null=True)),
                ('documento_solicitud', models.FileField(blank=True, null=True, upload_to='solicitudes/')),
                ('link_solicitud', models.URLField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tramitacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('presupuesto', models.CharField(max_length=200)),
                ('año', models.IntegerField()),
                ('nombre', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=200)),
                ('documento_tramitacion', models.FileField(blank=True, null=True, upload_to='tramitaciones/')),
                ('fecha_solicitud', models.CharField(blank=True, max_length=200, null=True)),
                ('fecha_recepcion', models.CharField(blank=True, max_length=200, null=True)),
                ('nota', models.TextField(blank=True, max_length=200, null=True)),
                ('descripcion', models.TextField(blank=True, max_length=10000, null=True)),
                ('link_tramitacion', models.URLField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]
