from django import forms
from .models import Proyecto,Solicitud,Tramitacion,Pago_tramitacion,Contactos,Insumos,PagoCliente, DetallePago
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


class PagoClienteForm(forms.ModelForm):
    class Meta:
        model = PagoCliente
        fields = [
            'proyecto', 'cliente_nombre', 'cliente_telefono', 'cliente_correo',
            'monto_total', 'fecha_vencimiento', 'descripcion', 'observaciones'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={'class': 'form-select select2'}),
            'cliente_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'cliente_telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'cliente_correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'cliente@email.com'}),
            'monto_total': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01', 
                'min': '0',
                'placeholder': '0.00'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Descripción del servicio o producto...'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2,
                'placeholder': 'Observaciones adicionales...'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si hay un proyecto seleccionado, pre-llenar datos del cliente
        if self.instance and self.instance.pk and hasattr(self.instance, 'proyecto') and self.instance.proyecto:
            proyecto = self.instance.proyecto
            if not self.instance.cliente_nombre:
                self.fields['cliente_nombre'].initial = proyecto.nombre
            if not self.instance.cliente_telefono:
                self.fields['cliente_telefono'].initial = proyecto.telefono
            if not self.instance.cliente_correo:
                self.fields['cliente_correo'].initial = proyecto.correo


class DetallePagoForm(forms.ModelForm):
    class Meta:
        model = DetallePago
        fields = [
            'fecha_pago', 'monto_pago', 'forma_pago', 
            'numero_referencia', 'comprobante_pago', 'notas'
        ]
        widgets = {
            'fecha_pago': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }),
            'monto_pago': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01', 
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'forma_pago': forms.Select(attrs={'class': 'form-select'}),
            'numero_referencia': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número de transferencia, cheque, etc.'
            }),
            'comprobante_pago': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3,
                'placeholder': 'Notas sobre este pago...'
            }),
        }

    def __init__(self, *args, **kwargs):
        pago_cliente = kwargs.pop('pago_cliente', None)
        super().__init__(*args, **kwargs)
        
        if pago_cliente:
            # Limitar el monto máximo al monto pendiente
            monto_pendiente = pago_cliente.monto_pendiente
            self.fields['monto_pago'].widget.attrs['max'] = str(monto_pendiente)
            self.fields['monto_pago'].help_text = f"Monto pendiente: ${monto_pendiente:,.2f}"

    def clean_monto_pago(self):
        monto_pago = self.cleaned_data.get('monto_pago')
        if hasattr(self, 'pago_cliente'):
            if monto_pago > self.pago_cliente.monto_pendiente:
                raise forms.ValidationError(
                    f"El monto no puede ser mayor al pendiente: ${self.pago_cliente.monto_pendiente:,.2f}"
                )
        return monto_pago


class BuscarPagoForm(forms.Form):
    """Formulario para filtros de búsqueda"""
    cliente = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre de cliente...'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[('', 'Todos los estados')] + PagoCliente.ESTADO_PAGO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        required=False,
        empty_label="Todos los proyectos",
        widget=forms.Select(attrs={'class': 'form-select select2'})
    )
    
    fecha_desde = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )