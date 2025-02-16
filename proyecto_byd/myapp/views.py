from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView,View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Proyecto,Solicitud,Contactos,Tramitacion,Pago_tramitacion,Listado,Insumos,Evento,Enlace,Boleta
from .forms import ProyectoForm, UserRegistrationForm,SolicitudForm,TramitacionForm,PagoTramitacionForm,ContactoForm,InsumoForm
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

        # Filtro por año
        if año:
            queryset = queryset.filter(año=año)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener todos los estados posibles
        estados = Proyecto._meta.get_field('estado_proyecto').choices
        estado_counts = {
            estado_key: Proyecto.objects.filter(estado_proyecto=estado_key).count()
            for estado_key, estado_label in estados
        }

        # Contadores generales para las tarjetas
        context['total_proyectos'] = Proyecto.objects.count()
        context['total_aprobados'] = Proyecto.objects.filter(estado_proyecto='Aprobado').count()
        context['total_no_concretados'] = Proyecto.objects.filter(estado_proyecto='No Concretado').count()
        context['total_ingresado'] = Proyecto.objects.filter(estado_proyecto='Ingresado').count()
        
        # Añadir estados al contexto
        context['estados'] = estados
        context['estado_counts'] = estado_counts
        
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