from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView,View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Proyecto,Solicitud,Contactos,Tramitacion,Pago_tramitacion,Listado,Insumos,Evento,Enlace,Boleta,PagoCliente, DetallePago
from .forms import ProyectoForm, UserRegistrationForm,SolicitudForm,TramitacionForm,PagoTramitacionForm,ContactoForm,InsumoForm,PagoClienteForm, DetallePagoForm, BuscarPagoForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.db.models import Sum
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import datetime
from django.template.loader import render_to_string
import calendar
from datetime import datetime
from django.core.paginator import Paginator
import openpyxl
from openpyxl.styles import Font, Border, Side
from django.db.models import Sum, Q
from django.contrib import messages
from decimal import Decimal



@method_decorator(login_required, name='dispatch')
class ProyectoListView(ListView):
    model = Proyecto
    template_name = 'myapp/proyecto_list.html'
    context_object_name = 'proyectos'
    ordering = ['-id']  # Orden descendente por ID

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        estado = self.request.GET.get('estado')
        proceso = self.request.GET.get('proceso')
        año = self.request.GET.get('año')

        # Búsqueda en varios campos
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(proyecto__icontains=query) |
                Q(direccion__icontains=query)
            )

        # Filtro por estado del proyecto
        if estado:
            queryset = queryset.filter(estado_proyecto=estado)

        # Filtro por proceso
        if proceso:
            queryset = queryset.filter(proceso=proceso)

        # Filtro por año
        if año:
            queryset = queryset.filter(año=año)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contadores generales para las tarjetas
        context['total_proyectos'] = Proyecto.objects.count()
        context['total_aprobados'] = Proyecto.objects.filter(estado_proyecto='aprobado').count()
        context['total_no_concretados'] = Proyecto.objects.filter(estado_proyecto='no_concretado').count()
        
        # Contador para "Trabajar en Proyecto" ← NUEVO CONTADOR
        context['total_trabajando'] = Proyecto.objects.filter(estado_proyecto='trabajando').count()
        
        # Actualizar el contador de ingresados para incluir todos los tipos
        context['total_ingresado'] = Proyecto.objects.filter(
            estado_proyecto__in=['ingreso_dom', 'ingresado_sag', 'ingresado_minvu', 
                               'ingresado_monumento', 'observado', 'rechazado']
        ).count()
        
        context['total_observados'] = Proyecto.objects.filter(estado_proyecto='observado').count()
        
        return context


@method_decorator(login_required, name='dispatch')
class ProyectoCreateView(CreateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'myapp/proyecto_create.html'
    success_url = reverse_lazy('proyecto-list')

@method_decorator(login_required, name='dispatch')
class ProyectoUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'myapp/proyecto_edit.html'
    success_url = reverse_lazy('proyecto-list')

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



# Vista para el login
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('proyecto-list')  # Redirige a la lista de proyectos
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Formulario inválido.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# Vista para el logout
def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirige al login

# Vista para el registro de usuarios
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Cuenta creada con éxito.")
            return redirect('login')  # Redirige al login después de registrarse
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



def analisis(request):
    # Contar proyectos en diferentes estados
    proyectos_completados = Proyecto.objects.filter(estado_proyecto='aprobado').count()
    proyectos_no_concretados = Proyecto.objects.filter(estado_proyecto='no_concretado').count()
    proyectos_obserbados = Proyecto.objects.filter(estado_proyecto='observado').count()
    ingresado = Proyecto.objects.filter(estado_proyecto='ingresado').count()
    
    # Contar clientes
    total_clientes = Proyecto.objects.count()  # Asegúrate de que el modelo Cliente existe

    context = {
        'proyectos_completados': proyectos_completados,
        'proyectos_no_concretados': proyectos_no_concretados,
        'total_clientes': total_clientes,
        'proyectos_obserbados': proyectos_obserbados,
        'ingresado': ingresado,

    }
    
    return render(request, 'myapp/analisis.html', context)


###############AVISTAS DEL MODELO SOLICITRUD######################

@method_decorator(login_required, name='dispatch')
class SolicitudListView(ListView):
    model = Solicitud
    template_name = 'solicitud/solicitud_list.html'
    context_object_name = 'solicitudes'
    ordering = ['-id']  # Orden descendente id

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        estado = self.request.GET.get('estado')

        # Filtro de búsqueda por solicitante, nombre y dirección
        if query:
            queryset = queryset.filter(
                Q(solicitante__icontains=query) | 
                Q(nombre__icontains=query) |
                Q(direccion__icontains=query) |
                Q(nombre_documento__icontains=query)
            )
        
        # Filtro por estado de solicitud
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
        
        # Obtener los contadores por estado
        context['completados_count'] = Solicitud.objects.filter(fecha_solicitud__isnull=False, fecha_recepcion__isnull=False).count()
        context['en_proceso_count'] = Solicitud.objects.filter(fecha_solicitud__isnull=False, fecha_recepcion__isnull=True).count()
        context['pendientes_count'] = Solicitud.objects.filter(fecha_solicitud__isnull=True).count()

        # Mantener los parámetros de búsqueda en el contexto para que se mantengan cuando se navegue entre páginas
        context['query'] = self.request.GET.get('q', '')
        context['estado'] = self.request.GET.get('estado', '')

        return context
    
@method_decorator(login_required, name='dispatch')
class SolicitudCreateView(CreateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitud/create_solicitud.html'
    success_url = reverse_lazy('solicitud-list')

@method_decorator(login_required, name='dispatch')
class SolicitudUpdateView(UpdateView):
    model = Solicitud
    form_class = SolicitudForm
    template_name = 'solicitud/edit_solicitud.html'
    success_url = reverse_lazy('solicitud-list')

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



@method_decorator(login_required, name='dispatch') # Vista de lista (index)  
class ContactosListView(ListView):  
    model = Contactos  
    form_class = ContactoForm
    template_name = 'contacto/contactos_list.html'  
    context_object_name = 'contactos'  
    ordering = ['-id']  # Orden descendente id
    
    def get_queryset(self):  
        queryset = super().get_queryset()  
        query = self.request.GET.get('q')  
        filtro_tipo = self.request.GET.get('tipo')  

        # Filtrar por búsqueda de nombre, correo o teléfono  
        if query:  
            queryset = queryset.filter(  
                Q(nombre__icontains=query) |   
                Q(correo__icontains=query) |   
                Q(telefono__icontains=query)  
            )  
        
        # Filtrar por tipo de contacto  
        if filtro_tipo:  
            queryset = queryset.filter(tipo=filtro_tipo)  # Cambiado a 'tipo'  

        return queryset  

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)  
        
        # Calcular los contadores  
        total_contactos = Contactos.objects.count()  
        total_clientes = Contactos.objects.filter(tipo='CLIENTE').count()  # Cambiado a 'tipo'  
        total_profesionales = Contactos.objects.filter(tipo='PROFESIONAL').count()  # Cambiado a 'tipo'  
        total_otros = Contactos.objects.filter(tipo='OTROS').count()  # Cambiado a 'tipo'  

        # Agregar los contadores al contexto  
        context['total_contactos'] = total_contactos  
        context['total_clientes'] = total_clientes  
        context['total_profesionales'] = total_profesionales  
        context['total_otros'] = total_otros  
        
        return context  

# Vista de detalle (ver)
@method_decorator(login_required, name='dispatch')
class ContactosDetailView(DetailView):
    model = Contactos
    template_name = 'contacto/contactos_detail.html'
    context_object_name = 'contacto'

# Vista de creación (crear)
@method_decorator(login_required, name='dispatch')
class ContactosCreateView(CreateView):
    model = Contactos
    template_name = 'contacto/contactos_create.html'
    fields = '__all__'
    success_url = reverse_lazy('contacto-list')  # Redirigir a la lista tras la creación

# Vista de actualización (editar)
@method_decorator(login_required, name='dispatch')
class ContactosUpdateView(UpdateView):
    model = Contactos
    template_name = 'contacto/contactos_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('contacto-list')

# Vista de eliminación (eliminar)
@method_decorator(login_required, name='dispatch')
class ContactosDeleteView(DeleteView):
    model = Contactos
    template_name = 'contacto/contactos_delete.html'
    success_url = reverse_lazy('contacto-list')


################## Vista de TRAMITACIONES ##########################33

@method_decorator(login_required, name='dispatch')
class TramitacionListView(ListView):
    model = Tramitacion
    template_name = 'tramitacion/tramitacion_list.html'
    context_object_name = 'tramitaciones'
    ordering = ['-id']  # Orden descendente id

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        estado = self.request.GET.get('estado')

        # Filtro de búsqueda por profesional y nombre de documento
        if query:
            queryset = queryset.filter(
                Q(profesional__icontains=query) | 
                Q(nombre_documento__icontains=query)
            )
        
        # Filtro por estado basado en 'fecha_recepcion'
        if estado:
            if estado == "completado":
                queryset = queryset.filter(fecha_recepcion__isnull=False)
            elif estado == "sin_fecha":
                queryset = queryset.filter(fecha_recepcion__isnull=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener los contadores por estado basado en 'fecha_recepcion'
        context['completados_count'] = Tramitacion.objects.filter(fecha_recepcion__isnull=False).count()
        context['sin_fecha_count'] = Tramitacion.objects.filter(fecha_recepcion__isnull=True).count()

        # Mantener los parámetros de búsqueda en el contexto
        context['query'] = self.request.GET.get('q', '')
        context['estado'] = self.request.GET.get('estado', '')

        return context

    
@method_decorator(login_required, name='dispatch')
class TramitacionCreateView(CreateView):
    model = Tramitacion
    form_class = TramitacionForm
    template_name = 'tramitacion/create_tramitacion.html'
    success_url = reverse_lazy('tramitacion-list')

@method_decorator(login_required, name='dispatch')
class TramitacionUpdateView(UpdateView):
    model = Tramitacion
    form_class = TramitacionForm
    template_name = 'tramitacion/edit_tramitacion.html'
    success_url = reverse_lazy('tramitacion-list')

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



#################################--FIN--######################################################


####################################---INGRESO Y EGRESO--##########################################################
@method_decorator(login_required, name='dispatch')
class PagoTramitacionListView(ListView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_list.html'
    context_object_name = 'pagos'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Obtener los filtros desde los parámetros GET
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        tipo_pago = self.request.GET.get('tipo_pago')

        # Aplicar filtros al queryset
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

        # Calcular totales
        total_ingresos = queryset.aggregate(Sum('ingreso'))['ingreso__sum'] or 0
        total_egresos = queryset.aggregate(Sum('egreso'))['egreso__sum'] or 0
        saldo = total_ingresos - total_egresos

        context.update({
            'total_ingresos_filtrados': total_ingresos,
            'total_egresos_filtrados': total_egresos,
            'saldo_filtrado': saldo,
        })
        return context
    
# Crear registro
@method_decorator(login_required, name='dispatch')
class PagoTramitacionCreateView(CreateView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_create.html'
    form_class = PagoTramitacionForm
    success_url = reverse_lazy('pago_tramitacion_list')

    def form_valid(self, form):
        # Aquí puedes agregar una validación personalizada si lo necesitas
        return super().form_valid(form)


# Editar registro
@method_decorator(login_required, name='dispatch')
class PagoTramitacionUpdateView(UpdateView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_edit.html'
    form_class = PagoTramitacionForm
    success_url = reverse_lazy('pago_tramitacion_list')

# Detalle de un registro
@method_decorator(login_required, name='dispatch')
class PagoTramitacionDetailView(DetailView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_detail.html'
    context_object_name = 'pago'

# Eliminar registro
@method_decorator(login_required, name='dispatch')
class PagoTramitacionDeleteView(DeleteView):
    model = Pago_tramitacion
    template_name = 'pago_tramitacion/pago_tramitacion_confirm_delete.html'
    success_url = reverse_lazy('pago_tramitacion_list')
    
#################################--FIN--######################################################


#################################listado######################################################

# Vista para listar todos los objetos
@method_decorator(login_required, name='dispatch')
class ListadoListView(ListView):
    model = Listado
    template_name = 'listado/listado_list.html'
    context_object_name = 'listados'
    ordering = ['-id']  # Orden descendente id

# Vista para crear un nuevo objeto
@method_decorator(login_required, name='dispatch')
class ListadoCreateView(CreateView):
    model = Listado
    template_name = 'listado/listado_create.html'
    fields = '__all__'
    success_url = reverse_lazy('listado_list')  # Redirige a la lista después de crear

# Vista para editar un objeto existente
@method_decorator(login_required, name='dispatch')
class ListadoUpdateView(UpdateView):
    model = Listado
    template_name = 'listado/listado_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('listado_list')

# Vista para ver los detalles de un objeto
@method_decorator(login_required, name='dispatch')
class ListadoDetailView(DetailView):
    model = Listado
    template_name = 'listado/listado_detail.html'
    context_object_name = 'listado'

# Eliminar registro
@method_decorator(login_required, name='dispatch')
class ListadoDeleteView(DeleteView):
    model = Listado
    template_name = 'listado/listado_delete.html'
    success_url = reverse_lazy('listado_list')
#################################--FIN--######################################################


##########################################--INSUMOS--#####################################################################33

@method_decorator(login_required, name='dispatch')
class InsumosListView(ListView):  
    model = Insumos  
    template_name = 'insumo/insumo_list.html'  # Cambia esto según el nombre de tu template  
    context_object_name = 'insumos'  # Nombre del contexto a usar en el template  
    ordering = ['-id']  # Orden descendente id

@method_decorator(login_required, name='dispatch')
class InsumosDetailView(DetailView):  
    model = Insumos  
    template_name = 'insumo/insumo_detail.html'  # Cambia esto según el nombre de tu template  
    context_object_name = 'insumo'  

@method_decorator(login_required, name='dispatch')
class InsumosCreateView(CreateView):  
    model = Insumos  
    template_name = 'insumo/insumo_create.html'  # Cambia esto según el nombre de tu template  
    form_class = InsumoForm
    success_url = reverse_lazy('insumo_list')  # Asegúrate de tener esta URL definida en tu urls.py  

@method_decorator(login_required, name='dispatch')
class InsumosUpdateView(UpdateView):  
    model = Insumos  
    template_name = 'insumo/insumo_edit.html'  # Usa el mismo que para Crear  
    form_class = InsumoForm
    success_url = reverse_lazy('insumo_list')  # Asegúrate de tener esta URL definida en tu urls.py  

@method_decorator(login_required, name='dispatch')
class InsumosDeleteView(DeleteView):  
    model = Insumos  
    template_name = 'insumo/insumo_delete.html'  # Cambia esto según el nombre de tu template  
    success_url = reverse_lazy('insumo_list')  # Asegúrate de tener esta URL definida en tu urls.py  
    #################################--FIN--######################################################



###############Calendario#####################3

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
    dias_del_mes = cal.itermonthdays2(anio, mes)  # Devuelve (día, día de la semana)
    dias = []
    semana = []

    for dia, dia_semana in dias_del_mes:
        if dia == 0:  # Día fuera del mes actual
            semana.append({"dia": "", "eventos": []})
        else:
            fecha_actual = datetime(anio, mes, dia).date()
            eventos = Evento.objects.filter(fecha=fecha_actual)
            semana.append({"dia": dia, "eventos": eventos})
        if len(semana) == 7:  # Semana completa
            dias.append(semana)
            semana = []

    if semana:  # Agregar la última semana incompleta
        dias.append(semana)

    # Manejo del formulario para agregar eventos
    if request.method == "POST" and "agregar_evento" in request.POST:
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")
        fecha_str = request.POST.get("fecha")

        try:
            # Convertir la fecha recibida al tipo Date
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()

            # Crear el evento
            Evento.objects.create(titulo=titulo, descripcion=descripcion, fecha=fecha)
            return redirect(f"/cuentas/calendario/?anio={anio}&mes={mes}")
        except ValueError:
            # En caso de error al convertir la fecha
            return redirect(f"/cuentas/calendario/?anio={anio}&mes={mes}&error=Fecha inválida")

    # Manejo de edición de eventos
    if request.method == "POST" and "editar_evento" in request.POST:
        evento_id = request.POST.get("evento_id")
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")

        evento = get_object_or_404(Evento, id=evento_id)
        evento.titulo = titulo
        evento.descripcion = descripcion
        evento.save()

        return redirect(f"/cuentas/calendario/?anio={anio}&mes={mes}")

    # Manejo de eliminación de eventos
    if request.method == "POST" and "eliminar_evento" in request.POST:
        evento_id = request.POST.get("evento_id")

        evento = get_object_or_404(Evento, id=evento_id)
        evento.delete()

        return redirect(f"/cuentas/calendario/?anio={anio}&mes={mes}")

    # Manejo de marcar/desmarcar el ticket (completado)
    if request.method == "POST" and "marcar_ticket" in request.POST:
        evento_id = request.POST.get("evento_id")
        evento = get_object_or_404(Evento, id=evento_id)
        evento.completado = True  # Marcar como completado
        evento.save()
        return redirect(f"/cuentas/calendario/?anio={anio}&mes={mes}")

    if request.method == "POST" and "desmarcar_ticket" in request.POST:
        evento_id = request.POST.get("evento_id")
        evento = get_object_or_404(Evento, id=evento_id)
        evento.completado = False  # Desmarcar como completado
        evento.save()
        return redirect(f"/cuentas/calendario/?anio={anio}&mes={mes}")

    # Contexto para la plantilla
    contexto = {
        'anio': anio,
        'mes': mes,
        'nombre_mes': calendar.month_name[mes],
        'dias': dias,
        'mes_anterior': mes_anterior,
        'anio_anterior': anio_anterior,
        'mes_siguiente': mes_siguiente,
        'anio_siguiente': anio_siguiente,
    }
    return render(request, 'actividades/calendario.html', contexto)
#################################--FIN--######################################################



#################################--VISTA DE ENLACE--######################################################
# Vista para listar los enlaces
class EnlaceListView(ListView):
    model = Enlace
    template_name = 'enlace/enlace_list.html'
    context_object_name = 'enlaces'
    ordering = ['-id']  # Orden descendente id

    def get_queryset(self):
        query = self.request.GET.get('q', '')  # Captura el parámetro de búsqueda
        object_list = Enlace.objects.filter(
            Q(titulo__icontains=query) | Q(description__icontains=query)  # Filtra por título o descripción
        ).order_by('-id')  # Ordena por el más reciente
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')  # Incluye el término de búsqueda en el contexto
        context['query'] = query
        context['total_enlaces'] = self.get_queryset().count()  # Total de enlaces
        context['current_page_count'] = len(context['enlaces'])  # Enlaces en la página actual
        return context

# Vista para crear un nuevo enlace
class EnlaceCreateView(CreateView):
    model = Enlace
    template_name = 'enlace/enlace_create.html'  # Cambia según la ubicación de tu plantilla
    fields = '__all__'
    success_url = reverse_lazy('enlace_list')

# Vista para actualizar un enlace existente
class EnlaceUpdateView(UpdateView):
    model = Enlace
    template_name = 'enlace/enlace_edit.html'  # Cambia según la ubicación de tu plantilla
    fields = '__all__'
    success_url = reverse_lazy('enlace_list')

# Vista para eliminar un enlace
class EnlaceDeleteView(DeleteView):
    model = Enlace
    template_name = 'enlace/enlace_delete.html'  # Cambia según la ubicación de tu plantilla
    success_url = reverse_lazy('enlace_list')

#################################--FIN--######################################################


class BoletaListView(ListView):
    model = Boleta
    template_name = 'boleta/boleta_list.html'
    context_object_name = 'boletas'
    ordering = ['-id']  # Orden descendente por id
    
class BoletaCreateView(CreateView):
    model = Boleta
    template_name = 'boleta/boleta_create.html'
    fields = '__all__'
    success_url = reverse_lazy('boleta_list')

class BoletaUpdateView(UpdateView):
    model = Boleta
    template_name = 'boleta/boleta_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('boleta_list')

class BoletaDeleteView(DeleteView):
    model = Boleta
    template_name = 'boleta/boleta_delete.html'
    success_url = reverse_lazy('boleta_list')


@method_decorator(login_required, name='dispatch')
class BoletaDetailView(DetailView):
    model = Boleta
    template_name = 'boleta/boleta_detail.html'
    context_object_name = 'boleta'


############ IMPORTACIONES DE EXCEL DE PROYECTOS #######################
def exportar_excel(request):
    # Crear un libro de Excel y una hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Proyectos'

    # Encabezados de la tabla
    headers = ['Pres', 'Año', 'Nombre', 'Proyecto', 'Dirección', 'Estado Proyecto', 'Detalle']
    ws.append(headers)

    # Estilo para los encabezados (negrita y borde)
    font = Font(bold=True)
    border = Border(
        top=Side(border_style="thin"),
        left=Side(border_style="thin"),
        right=Side(border_style="thin"),
        bottom=Side(border_style="thin")
    )
    
    # Aplicar estilo de encabezados
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = font
        cell.border = border

    # Obtener los datos de tu modelo
    proyectos = Proyecto.objects.all()

    # Agregar los datos de la tabla
    for proyecto in proyectos:
        ws.append([
            proyecto.presupuesto if proyecto.presupuesto else 'No disponible',
            proyecto.año if proyecto.año else 'No disponible',
            proyecto.nombre if proyecto.nombre else 'No disponible',
            proyecto.proyecto if proyecto.proyecto else 'No disponible',
            proyecto.direccion if proyecto.direccion else 'No disponible',
            proyecto.estado_proyecto if proyecto.estado_proyecto else 'No disponible',
            proyecto.detalle if proyecto.detalle else 'No disponible',
        ])

    # Ajustar el ancho de las columnas según el contenido
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Obtener la letra de la columna
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Crear la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=proyectos_exportados.xlsx'
    
    # Guardar el archivo en la respuesta
    wb.save(response)
    return response

################################### FIN  ##########################################


def exportar_tramitacion_excel(request):
    # Crear un libro de Excel y una hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Tramitaciones'

    # Encabezados de la tabla
    headers = [
        'Presupuesto', 'Año', 'Nombre', 'Dirección', 'Nota', 'N° Subdiv. Aprobada', 'Estado'
    ]
    ws.append(headers)

    # Estilo para los encabezados (negrita y borde)
    font = Font(bold=True)
    border = Border(
        top=Side(border_style="thin"),
        left=Side(border_style="thin"),
        right=Side(border_style="thin"),
        bottom=Side(border_style="thin")
    )
    
    # Aplicar estilo de encabezados
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = font
        cell.border = border

    # Obtener los datos de tu modelo
    tramitaciones = Tramitacion.objects.all()

    # Agregar los datos de la tabla
    for tramitacion in tramitaciones:
        ws.append([
            tramitacion.presupuesto,
            tramitacion.año,
            tramitacion.nombre,
            tramitacion.direccion,
            tramitacion.nota if tramitacion.nota else 'No disponible',
            'N° Subdiv. Aprobada' if tramitacion.documento_tramitacion else 'No disponible',  # Asume que 'N° Subdiv. Aprobada' es algo específico
            'Estado' if tramitacion.fecha_solicitud else 'Pendiente'  # Asume un estado simple basado en si hay o no fecha_solicitud
        ])

    # Ajustar el ancho de las columnas según el contenido
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter  # Obtener la letra de la columna
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # Crear la respuesta HTTP con el archivo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=tramitaciones_exportadas.xlsx'
    
    # Guardar el archivo en la respuesta
    wb.save(response)
    return response




# ============ VISTAS PARA PAGOS DE CLIENTES ============

@method_decorator(login_required, name='dispatch')
class PagoClienteListView(ListView):
    model = PagoCliente
    template_name = 'pagos_cliente/pago_cliente_list.html'
    context_object_name = 'pagos'
    ordering = ['-fecha_creacion']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Obtener parámetros de filtro
        cliente = self.request.GET.get('cliente')
        estado = self.request.GET.get('estado')
        proyecto_id = self.request.GET.get('proyecto')
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')

        # Aplicar filtros
        if cliente:
            queryset = queryset.filter(
                Q(cliente_nombre__icontains=cliente) |
                Q(proyecto__nombre__icontains=cliente)
            )
        
        if estado:
            queryset = queryset.filter(estado_pago=estado)
        
        if proyecto_id:
            queryset = queryset.filter(proyecto_id=proyecto_id)
        
        if fecha_desde:
            queryset = queryset.filter(fecha_creacion__date__gte=fecha_desde)
        
        if fecha_hasta:
            queryset = queryset.filter(fecha_creacion__date__lte=fecha_hasta)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Estadísticas generales
        queryset = self.get_queryset()
        context['total_pagos'] = queryset.count()
        context['total_monto'] = queryset.aggregate(Sum('monto_total'))['monto_total__sum'] or 0
        context['total_pagado'] = queryset.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0
        context['total_pendiente'] = context['total_monto'] - context['total_pagado']
        
        # Calcular promedio por cliente
        if context['total_pagos'] > 0:
            context['promedio_por_cliente'] = context['total_monto'] / context['total_pagos']
        else:
            context['promedio_por_cliente'] = 0
        
        # Contadores por estado
        context['pendientes_count'] = queryset.filter(estado_pago='pendiente').count()
        context['parciales_count'] = queryset.filter(estado_pago='parcial').count()
        context['completos_count'] = queryset.filter(estado_pago='completo').count()
        context['vencidos_count'] = queryset.filter(estado_pago='vencido').count()
        
        # Formulario de búsqueda
        context['form_buscar'] = BuscarPagoForm(self.request.GET)
        
        return context


@method_decorator(login_required, name='dispatch')
class PagoClienteCreateView(CreateView):
    model = PagoCliente
    form_class = PagoClienteForm
    template_name = 'pagos_cliente/pago_cliente_create.html'
    success_url = reverse_lazy('pago_cliente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pago de cliente creado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PagoClienteUpdateView(UpdateView):
    model = PagoCliente
    form_class = PagoClienteForm
    template_name = 'pagos_cliente/pago_cliente_edit.html'
    success_url = reverse_lazy('pago_cliente_list')

    def form_valid(self, form):
        messages.success(self.request, 'Pago de cliente actualizado exitosamente.')
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class PagoClienteDetailView(DetailView):
    model = PagoCliente
    template_name = 'pagos_cliente/pago_cliente_detail.html'
    context_object_name = 'pago'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['detalles_pago'] = self.object.detalles_pago.all().order_by('-fecha_pago')
        context['form_detalle_pago'] = DetallePagoForm()
        return context


@method_decorator(login_required, name='dispatch')
class PagoClienteDeleteView(DeleteView):
    model = PagoCliente
    template_name = 'pagos_cliente/pago_cliente_delete.html'
    success_url = reverse_lazy('pago_cliente_list')
    context_object_name = 'object'

    def delete(self, request, *args, **kwargs):
        try:
            pago = self.get_object()
            nombre_cliente = pago.cliente_nombre
            
            # Eliminar el objeto
            response = super().delete(request, *args, **kwargs)
            
            # Mensaje de éxito
            messages.success(request, f'Pago de {nombre_cliente} eliminado exitosamente.')
            return response
            
        except Exception as e:
            messages.error(request, f'Error al eliminar el pago: {str(e)}')
            return redirect('pago_cliente_detail', pk=self.kwargs['pk'])


# ============ VISTAS PARA DETALLES DE PAGO ============

@login_required
def crear_detalle_pago(request, pago_id):
    pago_cliente = get_object_or_404(PagoCliente, id=pago_id)
    
    if request.method == 'POST':
        form = DetallePagoForm(request.POST, request.FILES, pago_cliente=pago_cliente)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.pago_cliente = pago_cliente
            detalle.registrado_por = request.user
            
            # Verificar que no se exceda el monto pendiente
            if detalle.monto_pago > pago_cliente.monto_pendiente:
                messages.error(request, f'El monto no puede exceder el pendiente: ${pago_cliente.monto_pendiente:,.2f}')
                return redirect('pago_cliente_detail', pk=pago_id)
            
            detalle.save()
            messages.success(request, f'Pago de ${detalle.monto_pago:,.2f} registrado exitosamente.')
            return redirect('pago_cliente_detail', pk=pago_id)
        else:
            messages.error(request, 'Error en el formulario. Verifique los datos.')
    
    return redirect('pago_cliente_detail', pk=pago_id)


@login_required
def editar_detalle_pago(request, detalle_id):
    detalle = get_object_or_404(DetallePago, id=detalle_id)
    pago_cliente = detalle.pago_cliente
    
    if request.method == 'POST':
        form = DetallePagoForm(request.POST, request.FILES, instance=detalle, pago_cliente=pago_cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Detalle de pago actualizado exitosamente.')
            return redirect('pago_cliente_detail', pk=pago_cliente.id)
    else:
        form = DetallePagoForm(instance=detalle, pago_cliente=pago_cliente)
    
    return render(request, 'pagos_cliente/detalle_pago_edit.html', {
        'form': form,
        'detalle': detalle,
        'pago_cliente': pago_cliente
    })


@login_required
def eliminar_detalle_pago(request, detalle_id):
    detalle = get_object_or_404(DetallePago, id=detalle_id)
    pago_cliente = detalle.pago_cliente
    
    if request.method == 'POST':
        detalle.delete()
        messages.success(request, 'Detalle de pago eliminado exitosamente.')
    
    return redirect('pago_cliente_detail', pk=pago_cliente.id)


# ============ REPORTES Y EXPORTACIONES ============

@login_required
def reporte_pagos_cliente(request):
    """Vista para generar reportes de pagos"""
    
    # Obtener filtros
    form_buscar = BuscarPagoForm(request.GET)
    pagos = PagoCliente.objects.all()
    
    if form_buscar.is_valid():
        cliente = form_buscar.cleaned_data.get('cliente')
        estado = form_buscar.cleaned_data.get('estado')
        proyecto = form_buscar.cleaned_data.get('proyecto')
        fecha_desde = form_buscar.cleaned_data.get('fecha_desde')
        fecha_hasta = form_buscar.cleaned_data.get('fecha_hasta')
        
        if cliente:
            pagos = pagos.filter(
                Q(cliente_nombre__icontains=cliente) |
                Q(proyecto__nombre__icontains=cliente)
            )
        if estado:
            pagos = pagos.filter(estado_pago=estado)
        if proyecto:
            pagos = pagos.filter(proyecto=proyecto)
        if fecha_desde:
            pagos = pagos.filter(fecha_creacion__date__gte=fecha_desde)
        if fecha_hasta:
            pagos = pagos.filter(fecha_creacion__date__lte=fecha_hasta)
    
    # Estadísticas del reporte
    estadisticas = {
        'total_clientes': pagos.values('cliente_nombre').distinct().count(),
        'total_monto': pagos.aggregate(Sum('monto_total'))['monto_total__sum'] or 0,
        'total_pagado': pagos.aggregate(Sum('monto_pagado'))['monto_pagado__sum'] or 0,
        'total_pendiente': 0,
        'por_estado': {}
    }
    
    estadisticas['total_pendiente'] = estadisticas['total_monto'] - estadisticas['total_pagado']
    
    # Estadísticas por estado
    for estado, nombre in PagoCliente.ESTADO_PAGO_CHOICES:
        count = pagos.filter(estado_pago=estado).count()
        monto = pagos.filter(estado_pago=estado).aggregate(Sum('monto_total'))['monto_total__sum'] or 0
        estadisticas['por_estado'][estado] = {'count': count, 'monto': monto, 'nombre': nombre}
    
    context = {
        'pagos': pagos.order_by('-fecha_creacion'),
        'form_buscar': form_buscar,
        'estadisticas': estadisticas,
    }
    
# ============ API PARA OBTENER DATOS DEL PROYECTO ============

@login_required
def obtener_datos_proyecto(request, proyecto_id):
    """API para obtener datos del proyecto para auto-completar formulario"""
    try:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id)
        data = {
            'nombre': proyecto.nombre or '',
            'telefono': proyecto.telefono or '',
            'correo': proyecto.correo or '',
            'direccion': proyecto.direccion or '',
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


