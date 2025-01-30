from django import template
register = template.Library()

@register.filter
def field_icon(field_name):
    icons = {
        'solicitante': 'user',
        'nombre_documento': 'file-alt',
        'nombre': 'id-card',
        'direccion': 'map-marker-alt',
        'fecha_solicitud': 'calendar-alt',
        'fecha_recepcion': 'calendar-check',
        'descripcion': 'align-left',
        'documento_solicitud': 'file-upload',
        'link_solicitud': 'link',
    }
    return icons.get(field_name, 'info-circle')  # ícono por defecto



@register.filter(name='add_class')
def add_class(field, css_class):
    """Agrega una clase CSS a un campo de formulario"""
    return field.as_widget(attrs={"class": css_class})