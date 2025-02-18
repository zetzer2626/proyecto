from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class Proyecto(models.Model):
    ESTADO_PROYECTO_CHOICES = [
        ('no_concretado', 'No Concretado'),
        ('trabajando', 'Trabajar en Proyecto'),
        ('ingreso_dom', 'Ingresado DOM'),
        ('ingresado_sag', 'Ingresado SAG'),
        ('ingresado_minvu', 'Ingresado Minvu'),
        ('ingresado_monumento', 'Ingresado Monumento'),
        ('observado', 'Ingresado Observado'),
        ('rechazado', 'Ingresado Rechazado'),
        ('aprobado', 'Aprobado'),
        ('realizado', 'Realizado'),
        ('congelado', 'Congelado'),
    ]
    PROCESO_CHOICES = [
        ('terminado', 'Terminado'),
        ('No Aplica', 'No Aplica'),
        ('pendiente', 'Pendiente'),
    ]
    
    id = models.AutoField(primary_key=True)
    presupuesto = models.CharField(max_length=200,null=False,blank=False)
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=255,null=True,blank=True)
    correo = models.CharField(max_length=255,null=True,blank=True)
    direccion = models.CharField(max_length=255,null=True,blank=True)
    rol_avaluo = models.CharField(max_length=100,null=True,blank=True)
    año = models.IntegerField(null=True,blank=True)
    proyecto = models.CharField(max_length=255,null=True,blank=True)
    estado_proyecto = models.CharField(max_length=50, choices=ESTADO_PROYECTO_CHOICES,null=True,blank=True)
    detalle = models.TextField(max_length=10000,null=True,blank=True)
    descripcion = models.TextField(max_length=10000,null=True,blank=True)
    kardex = models.CharField(max_length=255,null=True,blank=True)
    proceso = models.CharField(max_length=20, choices=PROCESO_CHOICES,null=True,blank=True)
    
    # Documentos adicionales
    levantamiento = models.FileField(upload_to='documentos/', null=True , blank=True)
    escritura = models.FileField(upload_to='documentos/', null=True , blank=True)
    dominio_vigente = models.FileField(upload_to='documentos/', null=True , blank=True)
    cedula_identidad = models.FileField(upload_to='documentos/', null=True , blank=True)
    poder = models.FileField(upload_to='documentos/', null=True , blank=True)
    boleta_agua = models.FileField(upload_to='documentos/', null=True , blank=True)
    boleta_luz = models.FileField(upload_to='documentos/', null=True , blank=True)
    rol_avaluo_detallado = models.FileField(upload_to='documentos/', null=True , blank=True)
    proyecto_anterior = models.FileField(upload_to='documentos/', null=True , blank=True)
    conjunto_habitacional = models.FileField(upload_to='documentos/', null=True , blank=True)
    informe_previo = models.FileField(upload_to='documentos/', null=True , blank=True)
    utilidad_publica = models.FileField(upload_to='documentos/', null=True , blank=True)
    certificado_numero = models.FileField(upload_to='documentos/', null=True , blank=True)
    factibilidad = models.FileField(upload_to='documentos/', null=True , blank=True)
    seim = models.FileField(upload_to='documentos/', null=True , blank=True)
    listado = models.FileField(upload_to='documentos/', null=True , blank=True)
    
    # Ingresos
    opcional_1 = models.FileField(upload_to='opcional/', null=True, blank=True)
    opcional_2 = models.FileField(upload_to='opcional/', null=True, blank=True)
    opcional_3 = models.FileField(upload_to='opcional/', null=True, blank=True)
    opcional_4 = models.FileField(upload_to='opcional/', null=True, blank=True)
    opcional_5 = models.FileField(upload_to='opcional/', null=True, blank=True)
    opcional_6 = models.FileField(upload_to='opcional/', null=True, blank=True)
    opcional_7 = models.FileField(upload_to='opcional/', null=True, blank=True)
    opcional_8 = models.FileField(upload_to='opcional/', null=True, blank=True)
    opcional_9 = models.FileField(upload_to='opcional/', null=True, blank=True)
    opcional_10 = models.FileField(upload_to='opcional/', null=True, blank=True)

    # link Ondrive
    link_1 = models.URLField(max_length=500, blank=True, null=True)

    # link Nombres
    nombre_enlace_1 = models.CharField(max_length=255,null=True,blank=True)

    # Documentos Presupuesto y Link
    documento_presupuesto_1 = models.FileField(upload_to='presupuesto/', null=True, blank=True)
    documento_presupuesto_2 = models.FileField(upload_to='presupuesto/', null=True, blank=True)
    presupuesto_link= models.URLField(max_length=500, blank=True, null=True)
    enlace_documento = models.URLField(max_length=500, blank=True, null=True)
    
    # Nombres de Los Ingresos
    nombre_ingreso_1 = models.CharField(max_length=255,null=True,blank=True)
    nombre_ingreso_2 = models.CharField(max_length=255,null=True,blank=True)
    nombre_ingreso_3 = models.CharField(max_length=255,null=True,blank=True)
    nombre_ingreso_4 = models.CharField(max_length=255,null=True,blank=True)
    nombre_ingreso_5 = models.CharField(max_length=255,null=True,blank=True)
    nombre_ingreso_6 = models.CharField(max_length=255,null=True,blank=True)
    nombre_ingreso_7 = models.CharField(max_length=255,null=True,blank=True)
    nombre_ingreso_8 = models.CharField(max_length=255,null=True,blank=True)
    nombre_ingreso_9 = models.CharField(max_length=255,null=True,blank=True)
    nombre_ingreso_10 = models.CharField(max_length=255,null=True,blank=True)

    def calcular_porcentaje_completitud(self):
        total_campos = 16  # Total de campos que deseas evaluar
        campos_completos = 0
        
       # Verifica cada campo y cuenta los que están completos
        if self.levantamiento:
            campos_completos += 1
        if self.escritura:
            campos_completos += 1
        if self.dominio_vigente:
         campos_completos += 1
        if self.cedula_identidad:
         campos_completos += 1
        if self.poder:
         campos_completos += 1
        if self.boleta_agua:
          campos_completos += 1
        if self.boleta_luz:
         campos_completos += 1
        if self.rol_avaluo_detallado:
         campos_completos += 1
        if self.proyecto_anterior:
         campos_completos += 1
        if self.conjunto_habitacional:
         campos_completos += 1
        if self.informe_previo:
         campos_completos += 1
        if self.utilidad_publica:
         campos_completos += 1
        if self.certificado_numero:
         campos_completos += 1
        if self.factibilidad:
          campos_completos += 1
        if self.seim:
         campos_completos += 1
        if self.listado:
            campos_completos += 1

        return (campos_completos / total_campos) * 100  # Devuelve el porcentaje

    def __str__(self):
        return self.nombre

    
class Solicitud(models.Model):
    solicitante = models.CharField(max_length=200,null=False,blank=False)
    nombre_documento = models.CharField(max_length=200,null=False,blank=False)
    nombre = models.CharField(max_length=200,null=False,blank=False)
    direccion = models.CharField(max_length=200,null=True,blank=True)
    fecha_solicitud = models.CharField(max_length=200,null=True,blank=True)
    fecha_recepcion = models.CharField(max_length=200,null=True,blank=True)
    descripcion = models.TextField(max_length=10000,null=True,blank=True)
    documento_solicitud = models.FileField(upload_to='solicitudes/', null=True, blank=True)
    link_solicitud = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.nombre



class Contactos(models.Model):
    TIPO_CHOICES = [
        ('CLIENTE', 'Cliente'),
        ('CLIENTE PROYECTO', 'Cliente Proyecto'),
        ('CLIENTE LOTE', 'Cliente Lote'),
        ('PROFESIONAL', 'Profesional'),
        ('ENTIDAD', 'Entidad'),
        ('OTROS', 'Otros'),
    ]
    
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()

    def __str__(self):
        return self.nombre
    

class Tramitacion(models.Model):
    presupuesto = models.CharField(max_length=200,null=False,blank=False)
    año = models.IntegerField()
    nombre = models.CharField(max_length=200,null=False,blank=False)
    direccion = models.CharField(max_length=200,null=False,blank=False)
    documento_tramitacion = models.FileField(upload_to='tramitaciones/', null=True, blank=True)
    fecha_solicitud = models.CharField(max_length=200,null=True,blank=True)
    fecha_recepcion = models.CharField(max_length=200,null=True,blank=True)
    nota = models.TextField(max_length=200,null=True,blank=True)
    descripcion = models.TextField(max_length=10000,null=True,blank=True)
    link_tramitacion = models.URLField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return self.nombre

   

class Pago_tramitacion(models.Model):
      
    TIPO_PAGO_CHOICES = [
        ('ingreso', 'Ingreso'),
        ('egreso', 'Egreso'),
    ]
    tipo_pago = models.CharField(max_length=10, choices=TIPO_PAGO_CHOICES, default='ingreso')
    fecha = models.DateField(null=True, blank=True)  # Aquí está la corrección
    origen = models.CharField(max_length=100,null=True,blank=True)
    nombre = models.CharField(max_length=100,null=True,blank=True)
    gestion = models.TextField()
    ingreso= models.IntegerField(null=True, blank=True)
    egreso = models.IntegerField(null=True, blank=True)
    transferencia = models.FileField(upload_to='pago_tramitaciones/', null=True, blank=True)
    boletabyd = models.FileField(upload_to='pago_tramitaciones/', null=True, blank=True)
    facturabyd = models.FileField(upload_to='pago_tramitaciones/', null=True, blank=True)

    def __str__(self):
        return self.nombre




class Listado(models.Model):
   presupuesto = models.CharField(max_length=100,null=True,blank=True)
   año = models.CharField(max_length=10,null=True,blank=True)
   nombre = models.CharField(max_length=200,null=True,blank=True)
   gestion = models.TextField()
   nota = models.TextField()
   listado = models.URLField(max_length=500, blank=True, null=True)
   drive = models.URLField(max_length=500, blank=True, null=True) 

def __str__(self):
        return self.presupuesto

class Insumos(models.Model):
   solicitante = models.CharField(max_length=100,null=True,blank=True)
   descripcion = models.TextField()
   fecha_solicitud = models.CharField(max_length=200,null=True,blank=True)
   fecha_recepcion = models.CharField(max_length=200,null=True,blank=True)
   pago = models.FileField(upload_to='insumos/', null=True, blank=True)
   factura = models.FileField(upload_to='insumos/', null=True, blank=True)
   valor_total= models.IntegerField(null=True, blank=True)
   
def __str__(self):
        return self.solicitante


class Evento(models.Model):
    fecha = models.DateField()
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    completado = models.BooleanField(default=False)  # Campo para marcar como completado


    def __str__(self):
        return f"{self.titulo} - {self.fecha}"
    

class Enlace(models.Model):
   titulo = models.CharField(max_length=200, null=False,blank=False)
   description = models.TextField(max_length=5000, null=True, blank=True)
   link = models.URLField(max_length=500, blank=True, null=True) 
   documento_pdf = models.FileField(upload_to='pdf/', null=True, blank=True)
   avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # Nuevo campo de avatar

def __str__(self):
        return self.titulo


class Boleta(models.Model):
    ESTADO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('debito', 'Debito'),
        ('credito', 'Credito'),
        ('cheque', 'Cheque'),    
    ]
    presupuesto = models.CharField(max_length=100, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    monto = models.CharField(max_length=100, null=True, blank=True)
    correspondiente = models.TextField(max_length=1000, null=True, blank=True)
    fecha = models.CharField(max_length=200, null=True, blank=True)
    forma_pago = models.CharField(max_length=100, choices=ESTADO_CHOICES, null=True, blank=True)
    numero_talonario = models.CharField(max_length=100, null=True, blank=True)
    numero_cheque = models.CharField(max_length=100, null=True, blank=True)
    año = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Boleta {self.numero_talonario} - {self.nombre}"