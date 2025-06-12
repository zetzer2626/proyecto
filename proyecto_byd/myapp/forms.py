from django import forms
from .models import Proyecto,Solicitud,Tramitacion,Pago_tramitacion,Contactos,Insumos
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {
            'presupuesto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Presupuesto'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'rol_avaluo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rol Avalúo'}),
            'año': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Año'}),
            'proyecto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proyecto'}),
            'estado_proyecto': forms.Select(attrs={'class': 'form-control'}),
            'detalle': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Detalle'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'descripcion'}),
            'kardex': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kardex'}),
            'proceso': forms.Select(attrs={'class': 'form-control'}),

            # Documentos adicionales
            'levantamiento': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'escritura': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'dominio_vigente': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cedula_identidad': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'poder': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'boleta_agua': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'boleta_luz': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'rol_avaluo_detallado': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'proyecto_anterior': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'conjunto_habitacional': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'informe_previo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'utilidad_publica': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'certificado_numero': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'factibilidad': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'seim': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'listado': forms.ClearableFileInput(attrs={'class': 'form-control'}),

            # Ingresos
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

            # Links
            'link_1': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enlace Ondrive'}),

            'documento_presupuesto_1': forms.FileInput(attrs={'class': 'form-control'}),
            'documento_presupuesto_2': forms.FileInput(attrs={'class': 'form-control'}),
            'presupuesto_link': forms.URLInput(attrs={'class': 'form-control'}),
            'enlace_documento': forms.URLInput(attrs={'class': 'form-control'}),
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                self.fields['proceso'].initial = self.instance.proceso  # Mantener selección previa


class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = [
            'solicitante', 'nombre_documento', 'nombre', 'direccion', 
            'fecha_solicitud', 'fecha_recepcion', 'descripcion', 
            'documento_solicitud', 'link_solicitud'
        ]
        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del solicitante'}),
            'nombre_documento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del documento'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'fecha_solicitud': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_recepcion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 4}),
            'documento_solicitud': forms.FileInput(attrs={'class': 'form-control-file'}),
            'link_solicitud': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enlace al documento'}),
        }


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

class TramitacionForm(forms.ModelForm):
    class Meta:
        model = Tramitacion
        fields = '__all__'



class PagoTramitacionForm(forms.ModelForm): 
    class Meta:
        model = Pago_tramitacion
        fields = '__all__'
   

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contactos
        fields = ['nombre', 'tipo', 'telefono', 'correo']



class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumos  # Reemplaza con tu modelo
        fields = '__all__'
        widgets = {
            'solicitante': forms.TextInput(attrs={'class': 'form-control shadow-sm'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control shadow-sm'}),
            'fecha_solicitud': forms.DateInput(attrs={'class': 'form-control shadow-sm'}),
            'fecha_recepcion': forms.DateInput(attrs={'class': 'form-control shadow-sm'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control shadow-sm'}),
            'pago': forms.FileInput(attrs={'class': 'form-control shadow-sm'}),
            'factura': forms.FileInput(attrs={'class': 'form-control shadow-sm'}),
        }
