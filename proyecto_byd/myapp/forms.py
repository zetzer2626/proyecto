from django import forms
from .models import (Proyecto, Solicitud, Tramitacion, Pago_tramitacion, Contactos, 
                     Insumos, Evento, Enlace, Boleta, Listado)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import datetime


class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {
            # Información Básica
            'presupuesto': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: PRES-2024-001'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre completo del cliente',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+56 9 1234 5678'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'cliente@email.com'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Dirección completa del proyecto'
            }),
            'rol_avaluo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número de rol de avalúo'
            }),
            'año': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': datetime.datetime.now().year,
                'min': 2020,
                'max': 2030
            }),
            'proyecto': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descripción detallada del proyecto',
                'rows': 3
            }),
            
            # Estado y Proceso
            'estado_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'proceso': forms.Select(attrs={'class': 'form-control'}),
            'kardex': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número de kardex'
            }),
            'detalle': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Detalles adicionales del proyecto',
                'rows': 4
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descripción general',
                'rows': 4
            }),

            # Documentos principales
            'levantamiento': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.png'
            }),
            'escritura': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'dominio_vigente': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'cedula_identidad': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            }),
            'poder': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'boleta_agua': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            }),
            'boleta_luz': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            }),
            'rol_avaluo_detallado': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'proyecto_anterior': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'conjunto_habitacional': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'informe_previo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'utilidad_publica': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'certificado_numero': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'factibilidad': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'seim': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'listado': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx'
            }),

            # Documentos opcionales
            'opcional_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opcional_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opcional_3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opcional_4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opcional_5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opcional_6': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opcional_7': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opcional_8': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opcional_9': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'opcional_10': forms.ClearableFileInput(attrs={'class': 'form-control'}),

            # Enlaces
            'link_1': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://onedrive.com/...'
            }),
            'nombre_enlace_1': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre descriptivo del enlace'
            }),
            'presupuesto_link': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://enlace-presupuesto.com'
            }),
            'enlace_documento': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://documento.com'
            }),

            # Documentos de presupuesto
            'documento_presupuesto_1': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx'
            }),
            'documento_presupuesto_2': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx'
            }),

            # Nombres de ingresos
            'nombre_ingreso_1': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_ingreso_2': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_ingreso_3': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_ingreso_4': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_ingreso_5': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_ingreso_6': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_ingreso_7': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_ingreso_8': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_ingreso_9': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_ingreso_10': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Campos requeridos
        self.fields['nombre'].required = True
        
        # Ayuda contextual
        self.fields['presupuesto'].help_text = "Código único del presupuesto"
        self.fields['estado_proyecto'].help_text = "Estado actual del proyecto"
        self.fields['proceso'].help_text = "Estado del proceso administrativo"
        
        # Validaciones adicionales
        if self.instance and self.instance.pk:
            self.fields['proceso'].initial = self.instance.proceso

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo and '@' not in correo:
            raise forms.ValidationError("Ingrese un correo electrónico válido.")
        return correo

    def clean_año(self):
        año = self.cleaned_data.get('año')
        current_year = datetime.datetime.now().year
        if año and (año < 2020 or año > current_year + 5):
            raise forms.ValidationError(f"El año debe estar entre 2020 y {current_year + 5}")
        return año


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'solicitante', 'nombre_documento', 'nombre', 'direccion', 
            'fecha_solicitud', 'fecha_recepcion', 'descripcion', 
            'documento_solicitud', 'link_solicitud'
        ]
        widgets = {
            'solicitante': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre del solicitante'
            }),
            'nombre_documento': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre del documento solicitado'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre del cliente'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Dirección del proyecto'
            }),
            'fecha_solicitud': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'fecha_recepcion': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descripción detallada de la solicitud', 
                'rows': 4
            }),
            'documento_solicitud': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.png'
            }),
            'link_solicitud': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://enlace-al-documento.com'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_solicitud = cleaned_data.get('fecha_solicitud')
        fecha_recepcion = cleaned_data.get('fecha_recepcion')

        if fecha_solicitud and fecha_recepcion:
            if fecha_recepcion < fecha_solicitud:
                raise forms.ValidationError(
                    "La fecha de recepción no puede ser anterior a la fecha de solicitud."
                )
        return cleaned_data


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }), 
        label="Contraseña",
        min_length=8,
        help_text="Mínimo 8 caracteres"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        }), 
        label="Confirmar contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya existe.")
        return username


class TramitacionForm(forms.ModelForm):
    class Meta:
        model = Tramitacion
        fields = '__all__'
        widgets = {
            'presupuesto': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número de presupuesto'
            }),
            'año': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': datetime.datetime.now().year,
                'min': 2020,
                'max': 2030
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre del proyecto o cliente'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Dirección del proyecto'
            }),
            'documento_tramitacion': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'fecha_solicitud': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'fecha_recepcion': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'nota': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Notas adicionales',
                'rows': 3
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descripción detallada de la tramitación',
                'rows': 4
            }),
            'link_tramitacion': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://enlace-tramitacion.com'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_solicitud = cleaned_data.get('fecha_solicitud')
        fecha_recepcion = cleaned_data.get('fecha_recepcion')

        if fecha_solicitud and fecha_recepcion:
            if fecha_recepcion < fecha_solicitud:
                raise forms.ValidationError(
                    "La fecha de recepción no puede ser anterior a la fecha de solicitud."
                )
        return cleaned_data


class PagoTramitacionForm(forms.ModelForm):
    class Meta:
        model = Pago_tramitacion
        fields = '__all__'
        widgets = {
            'tipo_pago': forms.Select(attrs={
                'class': 'form-control'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'origen': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Origen del movimiento'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre descriptivo'
            }),
            'gestion': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descripción de la gestión realizada',
                'rows': 3
            }),
            'ingreso': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '0',
                'min': 0,
                'step': '0.01'
            }),
            'egreso': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '0',
                'min': 0,
                'step': '0.01'
            }),
            'transferencia': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            }),
            'boletabyd': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            }),
            'facturabyd': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default date to today
        if not self.instance.pk:
            self.fields['fecha'].initial = datetime.date.today()

    def clean(self):
        cleaned_data = super().clean()
        tipo_pago = cleaned_data.get('tipo_pago')
        ingreso = cleaned_data.get('ingreso')
        egreso = cleaned_data.get('egreso')

        if tipo_pago == 'ingreso':
            if not ingreso or ingreso <= 0:
                raise forms.ValidationError("Para un ingreso, debe especificar un monto mayor a 0.")
            if egreso and egreso > 0:
                cleaned_data['egreso'] = None
        elif tipo_pago == 'egreso':
            if not egreso or egreso <= 0:
                raise forms.ValidationError("Para un egreso, debe especificar un monto mayor a 0.")
            if ingreso and ingreso > 0:
                cleaned_data['ingreso'] = None

        return cleaned_data


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contactos
        fields = ['nombre', 'tipo', 'telefono', 'correo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre completo'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+56 9 1234 5678'
            }),
            'correo': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'correo@ejemplo.com'
            }),
        }

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo and '@' not in correo:
            raise forms.ValidationError("Ingrese un correo electrónico válido.")
        return correo


class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumos
        fields = '__all__'
        widgets = {
            'solicitante': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre del solicitante'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descripción detallada del insumo',
                'rows': 4
            }),
            'fecha_solicitud': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'fecha_recepcion': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'valor_total': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '0',
                'min': 0,
                'step': '0.01'
            }),
            'pago': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            }),
            'factura': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_solicitud = cleaned_data.get('fecha_solicitud')
        fecha_recepcion = cleaned_data.get('fecha_recepcion')

        if fecha_solicitud and fecha_recepcion:
            if fecha_recepcion < fecha_solicitud:
                raise forms.ValidationError(
                    "La fecha de recepción no puede ser anterior a la fecha de solicitud."
                )
        return cleaned_data


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['fecha', 'titulo', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Título del evento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descripción del evento (opcional)',
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default date to today
        if not self.instance.pk:
            self.fields['fecha'].initial = datetime.date.today()


class EnlaceForm(forms.ModelForm):
    class Meta:
        model = Enlace
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Título del enlace'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Descripción del enlace',
                'rows': 4
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'https://ejemplo.com'
            }),
            'documento_pdf': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.jpg,.png,.gif'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        link = cleaned_data.get('link')
        documento_pdf = cleaned_data.get('documento_pdf')

        if not link and not documento_pdf:
            raise forms.ValidationError(
                "Debe proporcionar al menos un enlace o un documento PDF."
            )
        return cleaned_data


class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = '__all__'
        widgets = {
            'presupuesto': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número de presupuesto'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nombre del cliente'
            }),
            'monto': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '$100.000'
            }),
            'correspondiente': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'A qué corresponde el pago',
                'rows': 3
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'forma_pago': forms.Select(attrs={
                'class': 'form-control'
            }),
            'numero_talonario': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número del talonario'
            }),
            'numero_cheque': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número del cheque (si aplica)'
            }),
            'año': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': datetime.datetime.now().year,
                'min': 2020,
                'max': 2030
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set defaults
        if not self.instance.pk:
            self.fields['fecha'].initial = datetime.date.today()
            self.fields['año'].initial = datetime.datetime.now().year

    def clean(self):
        cleaned_data = super().clean()
        forma_pago = cleaned_data.get('forma_pago')
        numero_cheque = cleaned_data.get('numero_cheque')

        if forma_pago == 'cheque' and not numero_cheque:
            raise forms.ValidationError(
                "Para pagos con cheque, debe especificar el número del cheque."
            )
        return cleaned_data


class ListadoForm(forms.ModelForm):
    class Meta:
        model = Listado
        fields = '__all__'
        widgets = {
            'presupuesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: PRES-2025-001'
            }),
            'año': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': str(datetime.datetime.now().year)
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre descriptivo del listado'
            }),
            'gestion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe las gestiones realizadas o por realizar',
                'rows': 4
            }),
            'nota': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Observaciones, comentarios o información adicional',
                'rows': 3
            }),
            'listado': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://enlace-al-listado.com'
            }),
            'drive': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://drive.google.com/...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Establecer año actual por defecto si es un nuevo registro
        if not self.instance.pk:
            self.fields['año'].initial = str(datetime.datetime.now().year)
        
        # Marcar campos requeridos
        self.fields['gestion'].required = True
        self.fields['nota'].required = True
        
        # Ayuda contextual
        self.fields['presupuesto'].help_text = "Código único del presupuesto"
        self.fields['año'].help_text = "Año del listado"
        self.fields['nombre'].help_text = "Título descriptivo del listado"
        self.fields['gestion'].help_text = "Describe las gestiones realizadas"
        self.fields['nota'].help_text = "Observaciones adicionales"
        self.fields['listado'].help_text = "URL del listado principal"
        self.fields['drive'].help_text = "Enlace a carpeta o archivo en Drive"

    def clean(self):
        cleaned_data = super().clean()
        gestion = cleaned_data.get('gestion')
        nota = cleaned_data.get('nota')
        
        if not gestion:
            raise forms.ValidationError("El campo Gestión es obligatorio.")
        
        if not nota:
            raise forms.ValidationError("El campo Notas es obligatorio.")
        
        return cleaned_data


# Formularios de búsqueda rápida
class BusquedaProyectoForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar proyectos...'
        })
    )
    estado = forms.ChoiceField(
        choices=[('', 'Todos')] + Proyecto.ESTADO_PROYECTO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    año = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Año'
        })
    )


class BusquedaContactoForm(forms.Form):
    q = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar contactos...'
        })
    )
    tipo = forms.ChoiceField(
        choices=[('', 'Todos')] + Contactos.TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class FiltroFechaForm(forms.Form):
    fecha_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    fecha_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


# Formulario para configuración del usuario
class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
        }


# Formulario para importación de datos
class ImportarDatosForm(forms.Form):
    archivo = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls,.csv'
        }),
        help_text="Formatos permitidos: Excel (.xlsx, .xls) o CSV"
    )
    tipo_importacion = forms.ChoiceField(
        choices=[
            ('proyectos', 'Proyectos'),
            ('contactos', 'Contactos'),
            ('tramitaciones', 'Tramitaciones'),
            ('insumos', 'Insumos'),
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sobrescribir = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Marcar si desea sobrescribir datos existentes"
    )