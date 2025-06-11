from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import (Proyecto, Solicitud, Contactos, Tramitacion, Pago_tramitacion, 
                     Listado, Insumos, Evento, Enlace, Boleta)
from .forms import (ProyectoForm, UserRegistrationForm, SolicitudForm, TramitacionForm,ListadoForm,
                    PagoTramitacionForm, ContactoForm, InsumoForm, EventoForm, EnlaceForm, BoletaForm)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum, Count
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import datetime, date
from django.template.loader import render_to_string
import calendar
import openpyxl
from openpyxl.styles import Font, Border, Side
import json


# ============= VISTAS DE PROYECTOS =============

@method_decorator(login_required, name='dispatch')
class ProyectoListView(ListView):
    model = Proyecto
    template_name = 'myapp/proyecto_list.html'
    context_object_name = 'proyectos'
    ordering = ['-id']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        estado = self.request.GET.get('estado')
        año = self.request.GET.get('año')
        proceso = self.request.GET.get('proceso')  # Nuevo filtro

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(proyecto__icontains=query) |
                Q(direccion__icontains=query) |
                Q(presupuesto__icontains=query) |
                Q(rol_avaluo__icontains=query) |
                Q(correo__icontains=query) |
                Q(telefono__icontains=query)
            )

        if estado:
            queryset = queryset.filter(estado_proyecto=estado)

        if año:
            queryset = queryset.filter(año=año)
            
        if proceso:  # Nuevo filtro
            queryset = queryset.filter(proceso=proceso)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contadores para las tarjetas
        context['total_proyectos'] = Proyecto.objects.count()
        context['total_aprobados'] = Proyecto.objects.filter(estado_proyecto='aprobado').count()
        context['total_no_concretados'] = Proyecto.objects.filter(estado_proyecto='no_concretado').count()
        context['total_observados'] = Proyecto.objects.filter(estado_proyecto='observado').count()
        context['total_ingresados'] = Proyecto.objects.filter(estado_proyecto__in=[
            'ingreso_dom', 'ingresado_sag', 'ingresado_minvu', 'ingresado_monumento'
        ]).count()
        
        # Agregar filtros actuales al contexto para mantenerlos en la paginación
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'estado': self.request.GET.get('estado', ''),
            'año': self.request.GET.get('año', ''),
            'proceso': self.request.GET.get('proceso', ''),
        }
        
        return context


@method_decorator(login_required, name='dispatch')
class ProyectoCreateView(CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'myapp/proyecto_create.html'
    success_url = reverse_lazy('proyecto-list')

    def form_valid(self, form):
        messages.success(self.request, 'Proyecto creado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProyectoUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'myapp/proyecto_edit.html'
    success_url = reverse_lazy('proyecto-list')

    def form_valid(self, form):
        messages.success(self.request, 'Proyecto actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProyectoDetailView(DetailView):
    model = Proyecto
    template_name = 'myapp/proyecto_detail.html'
    context_object_name = 'proyecto'


@method_decorator(login_required, name='dispatch')
class ProyectoDeleteView(DeleteView):
    model = Proyecto
    template_name = 'myapp/proyecto_confirm_delete.html'
    success_url = reverse_lazy('proyecto-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Proyecto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============= VISTAS DE AUTENTICACIÓN =============

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'proyecto-list')
                return redirect(next_url)
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Formulario inválido.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Cuenta creada con éxito.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


# ============= VISTAS DE ANÁLISIS =============

@login_required
def analisis(request):
    # Contadores básicos
    total_clientes = Proyecto.objects.count()
    proyectos_completados = Proyecto.objects.filter(estado_proyecto='aprobado').count()
    proyectos_no_concretados = Proyecto.objects.filter(estado_proyecto='no_concretado').count()
    proyectos_obserbados = Proyecto.objects.filter(estado_proyecto='observado').count()
    ingresado = Proyecto.objects.filter(estado_proyecto__in=[
        'ingreso_dom', 'ingresado_sag', 'ingresado_minvu', 'ingresado_monumento'
    ]).count()

    # Contadores adicionales para otras secciones
    total_solicitudes = Solicitud.objects.count()
    total_tramitaciones = Tramitacion.objects.count()
    total_contactos = Contactos.objects.count()
    
    # Estadísticas financieras
    total_ingresos = Pago_tramitacion.objects.filter(tipo_pago='ingreso').aggregate(
        total=Sum('ingreso'))['total'] or 0
    total_egresos = Pago_tramitacion.objects.filter(tipo_pago='egreso').aggregate(
        total=Sum('egreso'))['total'] or 0

    context = {
        'proyectos_completados': proyectos_completados,
        'proyectos_no_concretados': proyectos_no_concretados,
        'total_clientes': total_clientes,
        'proyectos_obserbados': proyectos_obserbados,
        'ingresado': ingresado,
        'total_solicitudes': total_solicitudes,
        'total_tramitaciones': total_tramitaciones,
        'total_contactos': total_contactos,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'saldo_total': total_ingresos - total_egresos,
    }
    
    return render(request, 'myapp/analisis.html', context)


# ============= VISTAS DE SOLICITUDES =============

@method_decorator(login_required, name='dispatch')
class SolicitudListView(ListView):
    model = Solicitud
    template_name = 'solicitud/solicitud_list.html'
    context_object_name = 'solicitudes'
    ordering = ['-id']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        estado = self.request.GET.get('estado')

        if query:
            queryset = queryset.filter(
                Q(solicitante__icontains=query) | 
                Q(nombre__icontains=query) |
                Q(direccion__icontains=query) |
                Q(nombre_documento__icontains=query)
            )
        
        if estado:
            if estado == "completado":
                queryset = queryset.filter(fecha_solicitud__isnull=False, fecha_recepcion__isnull=False)
            elif estado == "en_proceso":
                queryset = queryset.filter(fecha_solicitud__isnull=False, fecha_recepcion__isnull=True)
            elif estado == "pendiente":
                queryset = queryset.filter(fecha_solicitud__isnull=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['completados_count'] = Solicitud.objects.filter(
            fecha_solicitud__isnull=False, fecha_recepcion__isnull=False).count()
        context['en_proceso_count'] = Solicitud.objects.filter(
            fecha_solicitud__isnull=False, fecha_recepcion__isnull=True).count()
        context['pendientes_count'] = Solicitud.objects.filter(
            fecha_solicitud__isnull=True).count()

        context['query'] = self.request.GET.get('q', '')
        context['estado'] = self.request.GET.get('estado', '')

        return context


@method_decorator(login_required, name='dispatch')
class SolicitudCreateView(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitud/create_solicitud.html'
    success_url = reverse_lazy('solicitud-list')

    def form_valid(self, form):
        messages.success(self.request, 'Solicitud creada exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SolicitudUpdateView(UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitud/edit_solicitud.html'
    success_url = reverse_lazy('solicitud-list')

    def form_valid(self, form):
        messages.success(self.request, 'Solicitud actualizada exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class SolicitudDetailView(DetailView):
    model = Solicitud
    template_name = 'solicitud/detalle_solicitud.html'
    context_object_name = 'solicitud'


@method_decorator(login_required, name='dispatch')
class SolicitudDeleteView(DeleteView):
    model = Solicitud
    template_name = 'solicitud/delete_solicitud.html'
    success_url = reverse_lazy('solicitud-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Solicitud eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============= VISTAS DE CONTACTOS =============

@method_decorator(login_required, name='dispatch')
class ContactosListView(ListView):
    model = Contactos
    template_name = 'contacto/contactos_list.html'
    context_object_name = 'contactos'
    ordering = ['-id']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        filtro_tipo = self.request.GET.get('tipo')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(correo__icontains=query) |
                Q(telefono__icontains=query)
            )

        if filtro_tipo:
            queryset = queryset.filter(tipo=filtro_tipo)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['total_contactos'] = Contactos.objects.count()
        context['total_clientes'] = Contactos.objects.filter(tipo='CLIENTE').count()
        context['total_profesionales'] = Contactos.objects.filter(tipo='PROFESIONAL').count()
        context['total_otros'] = Contactos.objects.filter(tipo='OTROS').count()
        
        return context

    def post(self, request, *args, **kwargs):
        # Handle quick add from modal
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contacto agregado exitosamente.')
            return redirect('contacto-list')
        else:
            messages.error(request, 'Error al agregar contacto.')
            return self.get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ContactosDetailView(DetailView):
    model = Contactos
    template_name = 'contacto/contactos_detail.html'
    context_object_name = 'contacto'


@method_decorator(login_required, name='dispatch')
class ContactosCreateView(CreateView):
    model = Contactos
    template_name = 'contacto/contactos_create.html'
    form_class = ContactoForm
    success_url = reverse_lazy('contacto-list')

    def form_valid(self, form):
        messages.success(self.request, 'Contacto creado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ContactosUpdateView(UpdateView):
    model = Contactos
    template_name = 'contacto/contactos_edit.html'
    form_class = ContactoForm
    success_url = reverse_lazy('contacto-list')

    def form_valid(self, form):
        messages.success(self.request, 'Contacto actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ContactosDeleteView(DeleteView):
    model = Contactos
    template_name = 'contacto/contactos_delete.html'
    success_url = reverse_lazy('contacto-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Contacto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============= VISTAS DE TRAMITACIONES =============

@method_decorator(login_required, name='dispatch')
class TramitacionListView(ListView):
    model = Tramitacion
    template_name = 'tramitacion/tramitacion_list.html'
    context_object_name = 'tramitaciones'
    ordering = ['-id']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        estado = self.request.GET.get('estado')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(direccion__icontains=query) |
                Q(presupuesto__icontains=query)
            )
        
        if estado:
            if estado == "completado":
                queryset = queryset.filter(fecha_recepcion__isnull=False)
            elif estado == "sin_fecha":
                queryset = queryset.filter(fecha_recepcion__isnull=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['completados_count'] = Tramitacion.objects.filter(fecha_recepcion__isnull=False).count()
        context['sin_fecha_count'] = Tramitacion.objects.filter(fecha_recepcion__isnull=True).count()

        context['query'] = self.request.GET.get('q', '')
        context['estado'] = self.request.GET.get('estado', '')

        return context


@method_decorator(login_required, name='dispatch')
class TramitacionCreateView(CreateView):
    model = Tramitacion
    form_class = TramitacionForm
    template_name = 'tramitacion/create_tramitacion.html'
    success_url = reverse_lazy('tramitacion-list')

    def form_valid(self, form):
        messages.success(self.request, 'Tramitación creada exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TramitacionUpdateView(UpdateView):
    model = Tramitacion
    form_class = TramitacionForm
    template_name = 'tramitacion/edit_tramitacion.html'
    success_url = reverse_lazy('tramitacion-list')

    def form_valid(self, form):
        messages.success(self.request, 'Tramitación actualizada exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TramitacionDetailView(DetailView):
    model = Tramitacion
    template_name = 'tramitacion/detalle_tramitacion.html'
    context_object_name = 'tramitacion'


@method_decorator(login_required, name='dispatch')
class TramitacionDeleteView(DeleteView):
    model = Tramitacion
    template_name = 'tramitacion/delete_tramitacion.html'
    success_url = reverse_lazy('tramitacion-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Tramitación eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============= VISTAS DE PAGOS/INGRESOS/EGRESOS =============

@method_decorator(login_required, name='dispatch')
class PagoTramitacionListView(ListView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_list.html'
    context_object_name = 'pagos'
    ordering = ['-fecha', '-id']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        tipo_pago = self.request.GET.get('tipo_pago')

        if fecha_inicio:
            queryset = queryset.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha__lte=fecha_fin)
        if tipo_pago:
            queryset = queryset.filter(tipo_pago=tipo_pago)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        total_ingresos = queryset.filter(tipo_pago='ingreso').aggregate(Sum('ingreso'))['ingreso__sum'] or 0
        total_egresos = queryset.filter(tipo_pago='egreso').aggregate(Sum('egreso'))['egreso__sum'] or 0
        saldo = total_ingresos - total_egresos

        context.update({
            'total_ingresos_filtrados': total_ingresos,
            'total_egresos_filtrados': total_egresos,
            'saldo_filtrado': saldo,
        })
        return context


@method_decorator(login_required, name='dispatch')
class PagoTramitacionCreateView(CreateView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_create.html'
    form_class = PagoTramitacionForm
    success_url = reverse_lazy('pago_tramitacion_list')

    def get_initial(self):
        initial = super().get_initial()
        tipo = self.request.GET.get('tipo')
        if tipo in ['ingreso', 'egreso']:
            initial['tipo_pago'] = tipo
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Movimiento financiero registrado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PagoTramitacionUpdateView(UpdateView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_edit.html'
    form_class = PagoTramitacionForm
    success_url = reverse_lazy('pago_tramitacion_list')

    def form_valid(self, form):
        messages.success(self.request, 'Movimiento financiero actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PagoTramitacionDetailView(DetailView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_detail.html'
    context_object_name = 'pago'


@method_decorator(login_required, name='dispatch')
class PagoTramitacionDeleteView(DeleteView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_confirm_delete.html'
    success_url = reverse_lazy('pago_tramitacion_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Movimiento financiero eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============= VISTAS DE LISTADOS =============

@method_decorator(login_required, name='dispatch')
class ListadoListView(ListView):
    model = Listado
    template_name = 'listado/listado_list.html'
    context_object_name = 'listados'
    ordering = ['-id']
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        año = self.request.GET.get('año')
        orden = self.request.GET.get('orden', '-id')

        if query:
            queryset = queryset.filter(
                Q(presupuesto__icontains=query) |
                Q(nombre__icontains=query) |
                Q(gestion__icontains=query)
            )

        if año:
            queryset = queryset.filter(año=año)

        if orden:
            queryset = queryset.order_by(orden)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['con_enlaces'] = Listado.objects.filter(listado__isnull=False).exclude(listado='').count()
        context['con_drive'] = Listado.objects.filter(drive__isnull=False).exclude(drive='').count()
        
        # Agregar filtros actuales al contexto para mantenerlos en la paginación
        context['current_filters'] = {
            'q': self.request.GET.get('q', ''),
            'año': self.request.GET.get('año', ''),
            'orden': self.request.GET.get('orden', ''),
        }
        
        return context


@method_decorator(login_required, name='dispatch')
class ListadoCreateView(CreateView):
    model = Listado
    form_class = ListadoForm  # ← Cambiado de fields a form_class
    template_name = 'listado/listado_create.html'
    success_url = reverse_lazy('listado_list')

    def form_valid(self, form):
        messages.success(self.request, 'Listado creado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ListadoUpdateView(UpdateView):
    model = Listado
    form_class = ListadoForm  # ← Cambiado de fields a form_class
    template_name = 'listado/listado_edit.html'
    success_url = reverse_lazy('listado_list')

    def form_valid(self, form):
        messages.success(self.request, 'Listado actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ListadoDetailView(DetailView):
    model = Listado
    template_name = 'listado/listado_detail.html'
    context_object_name = 'listado'


@method_decorator(login_required, name='dispatch')
class ListadoDeleteView(DeleteView):
    model = Listado
    template_name = 'listado/listado_delete.html'
    success_url = reverse_lazy('listado_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Listado eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============= VISTAS DE INSUMOS =============

@method_decorator(login_required, name='dispatch')
class InsumosListView(ListView):
    model = Insumos
    template_name = 'insumo/insumo_list.html'
    context_object_name = 'insumos'
    ordering = ['-id']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        estado = self.request.GET.get('estado')

        if query:
            queryset = queryset.filter(
                Q(solicitante__icontains=query) |
                Q(descripcion__icontains=query)
            )

        if estado:
            if estado == "completado":
                queryset = queryset.filter(fecha_solicitud__isnull=False, fecha_recepcion__isnull=False)
            elif estado == "pendiente":
                queryset = queryset.filter(fecha_solicitud__isnull=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calcular estadísticas
        total_valor = Insumos.objects.aggregate(Sum('valor_total'))['valor_total__sum'] or 0
        count = Insumos.objects.count()
        promedio_valor = total_valor / count if count > 0 else 0
        
        context['total_valor'] = total_valor
        context['promedio_valor'] = promedio_valor
        context['completados_count'] = Insumos.objects.filter(
            fecha_solicitud__isnull=False, fecha_recepcion__isnull=False).count()
        context['en_proceso_count'] = Insumos.objects.filter(
            fecha_solicitud__isnull=False, fecha_recepcion__isnull=True).count()
        context['pendientes_count'] = Insumos.objects.filter(
            fecha_solicitud__isnull=True).count()
        
        return context


@method_decorator(login_required, name='dispatch')
class InsumosDetailView(DetailView):
    model = Insumos
    template_name = 'insumo/insumo_detail.html'
    context_object_name = 'insumo'


@method_decorator(login_required, name='dispatch')
class InsumosCreateView(CreateView):
    model = Insumos
    template_name = 'insumo/insumo_create.html'
    form_class = InsumoForm
    success_url = reverse_lazy('insumo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Insumo creado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class InsumosUpdateView(UpdateView):
    model = Insumos
    template_name = 'insumo/insumo_edit.html'
    form_class = InsumoForm
    success_url = reverse_lazy('insumo_list')

    def form_valid(self, form):
        messages.success(self.request, 'Insumo actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class InsumosDeleteView(DeleteView):
    model = Insumos
    template_name = 'insumo/insumo_delete.html'
    success_url = reverse_lazy('insumo_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Insumo eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============= VISTAS DE ENLACES =============

@method_decorator(login_required, name='dispatch')
class EnlaceListView(ListView):
    model = Enlace
    template_name = 'enlace/enlace_list.html'
    context_object_name = 'enlaces'
    ordering = ['-id']
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        object_list = Enlace.objects.filter(
            Q(titulo__icontains=query) | Q(description__icontains=query)
        ).order_by('-id')
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query
        context['total_enlaces'] = self.get_queryset().count()
        context['current_page_count'] = len(context['enlaces'])
        return context


@method_decorator(login_required, name='dispatch')
class EnlaceCreateView(CreateView):
    model = Enlace
    template_name = 'enlace/enlace_create.html'
    form_class = EnlaceForm
    success_url = reverse_lazy('enlace_list')

    def form_valid(self, form):
        messages.success(self.request, 'Enlace creado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EnlaceUpdateView(UpdateView):
    model = Enlace
    template_name = 'enlace/enlace_edit.html'
    form_class = EnlaceForm
    success_url = reverse_lazy('enlace_list')

    def form_valid(self, form):
        messages.success(self.request, 'Enlace actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class EnlaceDeleteView(DeleteView):
    model = Enlace
    template_name = 'enlace/enlace_delete.html'
    success_url = reverse_lazy('enlace_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Enlace eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)


# ============= VISTAS DE BOLETAS =============

@method_decorator(login_required, name='dispatch')
class BoletaListView(ListView):
    model = Boleta
    template_name = 'boleta/boleta_list.html'
    context_object_name = 'boletas'
    ordering = ['-id']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        forma_pago = self.request.GET.get('forma_pago')
        año = self.request.GET.get('año')

        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(presupuesto__icontains=query) |
                Q(numero_talonario__icontains=query)
            )

        if forma_pago:
            queryset = queryset.filter(forma_pago=forma_pago)

        if año:
            queryset = queryset.filter(año=año)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contadores por forma de pago
        context['efectivo_count'] = Boleta.objects.filter(forma_pago='efectivo').count()
        context['transferencia_count'] = Boleta.objects.filter(forma_pago='transferencia').count()
        context['debito_count'] = Boleta.objects.filter(forma_pago='debito').count()
        context['credito_count'] = Boleta.objects.filter(forma_pago='credito').count()
        context['cheque_count'] = Boleta.objects.filter(forma_pago='cheque').count()
        
        return context


@method_decorator(login_required, name='dispatch')
class BoletaCreateView(CreateView):
    model = Boleta
    template_name = 'boleta/boleta_create.html'
    form_class = BoletaForm
    success_url = reverse_lazy('boleta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Boleta creada exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BoletaUpdateView(UpdateView):
    model = Boleta
    template_name = 'boleta/boleta_edit.html'
    form_class = BoletaForm
    success_url = reverse_lazy('boleta_list')

    def form_valid(self, form):
        messages.success(self.request, 'Boleta actualizada exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BoletaDeleteView(DeleteView):
    model = Boleta
    template_name = 'boleta/boleta_delete.html'
    success_url = reverse_lazy('boleta_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Boleta eliminada exitosamente.')
        return super().delete(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class BoletaDetailView(DetailView):
    model = Boleta
    template_name = 'boleta/boleta_detail.html'
    context_object_name = 'boleta'


# ============= VISTA DEL CALENDARIO =============

@login_required
def calendario(request):
    # Obtener el año y el mes desde la URL o usar los valores actuales
    anio = int(request.GET.get('anio', datetime.now().year))
    mes = int(request.GET.get('mes', datetime.now().month))

    # Calcular mes anterior y siguiente
    mes_anterior = mes - 1 if mes > 1 else 12
    anio_anterior = anio if mes > 1 else anio - 1
    mes_siguiente = mes + 1 if mes < 12 else 1
    anio_siguiente = anio if mes < 12 else anio + 1

    # Generar el calendario
    cal = calendar.Calendar()
    dias_del_mes = cal.itermonthdays2(anio, mes)
    dias = []
    semana = []

    for dia, dia_semana in dias_del_mes:
        if dia == 0:
            semana.append({"dia": "", "eventos": []})
        else:
            fecha_actual = datetime(anio, mes, dia).date()
            eventos = Evento.objects.filter(fecha=fecha_actual)
            semana.append({"dia": dia, "eventos": eventos})
        if len(semana) == 7:
            dias.append(semana)
            semana = []

    if semana:
        dias.append(semana)

    # Manejo del formulario para agregar eventos
    if request.method == "POST" and "agregar_evento" in request.POST:
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        fecha_str = request.POST.get("fecha")

        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            Evento.objects.create(titulo=titulo, descripcion=descripcion, fecha=fecha)
            messages.success(request, 'Evento creado exitosamente.')
            return redirect(f"calendario/?anio={anio}&mes={mes}")
        except ValueError:
            messages.error(request, 'Fecha inválida.')
            return redirect(f"calendario/?anio={anio}&mes={mes}")

    # Manejo de edición de eventos
    if request.method == "POST" and "editar_evento" in request.POST:
        evento_id = request.POST.get("evento_id")
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")

        evento = get_object_or_404(Evento, id=evento_id)
        evento.titulo = titulo
        evento.descripcion = descripcion
        evento.save()
        messages.success(request, 'Evento actualizado exitosamente.')

        return redirect(f"calendario/?anio={anio}&mes={mes}")

    # Manejo de eliminación de eventos
    if request.method == "POST" and "eliminar_evento" in request.POST:
        evento_id = request.POST.get("evento_id")
        evento = get_object_or_404(Evento, id=evento_id)
        evento.delete()
        messages.success(request, 'Evento eliminado exitosamente.')

        return redirect(f"calendario/?anio={anio}&mes={mes}")

    # Manejo de marcar/desmarcar el ticket (completado)
    if request.method == "POST" and "marcar_ticket" in request.POST:
        evento_id = request.POST.get("evento_id")
        evento = get_object_or_404(Evento, id=evento_id)
        evento.completado = True
        evento.save()
        messages.success(request, 'Evento marcado como completado.')
        return redirect(f"calendario/?anio={anio}&mes={mes}")

    if request.method == "POST" and "desmarcar_ticket" in request.POST:
        evento_id = request.POST.get("evento_id")
        evento = get_object_or_404(Evento, id=evento_id)
        evento.completado = False
        evento.save()
        messages.success(request, 'Evento desmarcado como completado.')
        return redirect(f"calendario/?anio={anio}&mes={mes}")

    # Obtener eventos del mes para el panel lateral
    primer_dia_mes = datetime(anio, mes, 1).date()
    if mes == 12:
        ultimo_dia_mes = datetime(anio + 1, 1, 1).date() - timezone.timedelta(days=1)
    else:
        ultimo_dia_mes = datetime(anio, mes + 1, 1).date() - timezone.timedelta(days=1)
    
    eventos_mes = Evento.objects.filter(fecha__range=[primer_dia_mes, ultimo_dia_mes]).order_by('fecha')
    
    # Calcular estadísticas
    total_eventos = eventos_mes.count()
    eventos_completados = eventos_mes.filter(completado=True).count()
    eventos_pendientes = total_eventos - eventos_completados
    porcentaje_completado = (eventos_completados / total_eventos * 100) if total_eventos > 0 else 0

    contexto = {
        'anio': anio,
        'mes': mes,
        'nombre_mes': calendar.month_name[mes],
        'dias': dias,
        'mes_anterior': mes_anterior,
        'anio_anterior': anio_anterior,
        'mes_siguiente': mes_siguiente,
        'anio_siguiente': anio_siguiente,
        'eventos_mes': eventos_mes,
        'total_eventos': total_eventos,
        'eventos_completados': eventos_completados,
        'eventos_pendientes': eventos_pendientes,
        'porcentaje_completado': round(porcentaje_completado),
        'today': date.today(),
    }
    return render(request, 'actividades/calendario.html', contexto)


# ============= FUNCIONES DE EXPORTACIÓN =============

@login_required
def exportar_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Proyectos'

    headers = ['Presupuesto', 'Año', 'Nombre', 'Proyecto', 'Dirección', 'Estado Proyecto', 'Detalle']
    ws.append(headers)

    font = Font(bold=True)
    border = Border(
        top=Side(border_style="thin"),
        left=Side(border_style="thin"),
        right=Side(border_style="thin"),
        bottom=Side(border_style="thin")
    )
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = font
        cell.border = border

    proyectos = Proyecto.objects.all()

    for proyecto in proyectos:
        ws.append([
            proyecto.presupuesto if proyecto.presupuesto else 'No disponible',
            proyecto.año if proyecto.año else 'No disponible',
            proyecto.nombre if proyecto.nombre else 'No disponible',
            proyecto.proyecto if proyecto.proyecto else 'No disponible',
            proyecto.direccion if proyecto.direccion else 'No disponible',
            proyecto.get_estado_proyecto_display() if proyecto.estado_proyecto else 'No disponible',
            proyecto.detalle if proyecto.detalle else 'No disponible',
        ])

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=proyectos_exportados.xlsx'
    
    wb.save(response)
    return response


@login_required
def exportar_tramitacion_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Tramitaciones'

    headers = [
        'Presupuesto', 'Año', 'Nombre', 'Dirección', 'Nota', 'Fecha Solicitud', 'Fecha Recepción', 'Estado'
    ]
    ws.append(headers)

    font = Font(bold=True)
    border = Border(
        top=Side(border_style="thin"),
        left=Side(border_style="thin"),
        right=Side(border_style="thin"),
        bottom=Side(border_style="thin")
    )
    
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = font
        cell.border = border

    tramitaciones = Tramitacion.objects.all()

    for tramitacion in tramitaciones:
        estado = 'Completado' if tramitacion.fecha_recepcion else 'Pendiente'
        ws.append([
            tramitacion.presupuesto,
            tramitacion.año,
            tramitacion.nombre,
            tramitacion.direccion,
            tramitacion.nota if tramitacion.nota else 'No disponible',
            tramitacion.fecha_solicitud if tramitacion.fecha_solicitud else 'No disponible',
            tramitacion.fecha_recepcion if tramitacion.fecha_recepcion else 'No disponible',
            estado
        ])

    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=tramitaciones_exportadas.xlsx'
    
    wb.save(response)
    return response


# ============= VISTAS API/AJAX =============

@login_required
def marcar_insumo_completado(request, insumo_id):
    """Vista AJAX para marcar insumo como completado"""
    if request.method == 'POST':
        try:
            insumo = get_object_or_404(Insumos, id=insumo_id)
            insumo.fecha_recepcion = date.today().strftime('%Y-%m-%d')
            insumo.save()
            return JsonResponse({'success': True, 'message': 'Insumo marcado como completado'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@login_required
def estadisticas_dashboard(request):
    """Vista AJAX para obtener estadísticas del dashboard"""
    data = {
        'proyectos': {
            'total': Proyecto.objects.count(),
            'aprobados': Proyecto.objects.filter(estado_proyecto='aprobado').count(),
            'observados': Proyecto.objects.filter(estado_proyecto='observado').count(),
            'no_concretados': Proyecto.objects.filter(estado_proyecto='no_concretado').count(),
        },
        'financiero': {
            'ingresos': Pago_tramitacion.objects.filter(tipo_pago='ingreso').aggregate(
                Sum('ingreso'))['ingreso__sum'] or 0,
            'egresos': Pago_tramitacion.objects.filter(tipo_pago='egreso').aggregate(
                Sum('egreso'))['egreso__sum'] or 0,
        },
        'otros': {
            'solicitudes': Solicitud.objects.count(),
            'tramitaciones': Tramitacion.objects.count(),
            'contactos': Contactos.objects.count(),
        }
    }
    return JsonResponse(data)