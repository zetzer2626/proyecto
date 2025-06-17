from django.urls import path
from .views import * 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Proyectos
    path('', ProyectoListView.as_view(), name='proyecto-list'),
    path('proyectos/nuevo/', ProyectoCreateView.as_view(), name='proyecto-create'),  # Crear proyecto
    path('proyectos/<int:pk>/', ProyectoDetailView.as_view(), name='proyecto-detail'),  # Detalles del proyecto
    path('proyectos/<int:pk>/editar/', ProyectoUpdateView.as_view(), name='proyecto-update'),  # Editar proyecto
    path('proyectos/<int:pk>/eliminar/', ProyectoDeleteView.as_view(), name='proyecto-delete'),  # Eliminar proyecto
   

    # Solicitudes
    path('solicitudes/', SolicitudListView.as_view(), name='solicitud-list'),
    path('solicitudes/nuevo/', SolicitudCreateView.as_view(), name='solicitud-create'),  # Crear pago
    path('solicitudes/<int:pk>/editar/', SolicitudUpdateView.as_view(), name='solicitud-update'),  # Editar pago
    path('solicitudes/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud-detail'),
    path('solicitudes/eliminar/<int:pk>/', SolicitudDeleteView.as_view(), name='solicitud-delete'),

    # Autenticación
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),


    # Analisis de conteo
    path('analisis/', analisis, name='analisis'),

    # Contactos
    path('contactos/', ContactosListView.as_view(), name='contacto-list'),
    path('contactos/nuevo/', ContactosCreateView.as_view(), name='contacto-create'),  # Crear 
    path('contactos/<int:pk>/editar/', ContactosUpdateView.as_view(), name='contacto-update'),  # Editar 
    path('contactos/<int:pk>/', ContactosDetailView.as_view(), name='contacto-detail'),
    path('contactos/eliminar/<int:pk>/', ContactosDeleteView.as_view(), name='contacto-delete'),

    # Tramitaciones
    path('tramitaciones/', TramitacionListView.as_view(), name='tramitacion-list'),
    path('tramitaciones/nuevo/', TramitacionCreateView.as_view(), name='tramitacion-create'),  # Crear pago
    path('tramitaciones/<int:pk>/editar/', TramitacionUpdateView.as_view(), name='tramitacion-update'),  # Editar pago
    path('tramitaciones/<int:pk>/', TramitacionDetailView.as_view(), name='tramitacion-detail'),
    path('tramitaciones/eliminar/<int:pk>/', TramitacionDeleteView.as_view(), name='tramitacion-delete'),


    path('pagotramitacion/', PagoTramitacionListView.as_view(), name='pago_tramitacion_list'),
    path('crear/', PagoTramitacionCreateView.as_view(), name='pago_tramitacion_create'),
    path('editar/<int:pk>/', PagoTramitacionUpdateView.as_view(), name='pago_tramitacion_edit'),
    path('detalle/<int:pk>/', PagoTramitacionDetailView.as_view(), name='pago_tramitacion_detail'),
    path('eliminar/<int:pk>/', PagoTramitacionDeleteView.as_view(), name='pago_tramitacion_delete'),


    # Listado
    path('listado/', views.ListadoListView.as_view(), name='listado_list'),  # Lista de objetos
    path('nuevo/', views.ListadoCreateView.as_view(), name='listado_create'),  # Crear nuevo objeto
    path('editarlo/<int:pk>/', views.ListadoUpdateView.as_view(), name='listado_edit'),  # Editar objeto
    path('detalles/<int:pk>/', views.ListadoDetailView.as_view(), name='listado_detail'),  # Ver detalles del objeto
    path('eliminarlo/<int:pk>/', ListadoDeleteView.as_view(), name='listado_delete'),

    #insumo
    path('insumo/', InsumosListView.as_view(), name='insumo_list'),  
    path('insumodetalle<int:pk>/', InsumosDetailView.as_view(), name='insumo_detail'),  
    path('insumocreate/', InsumosCreateView.as_view(), name='insumo_create'),  
    path('insumoupdate/<int:pk>/', InsumosUpdateView.as_view(), name='insumo_edit'),  
    path('insumodelete/<int:pk>/', InsumosDeleteView.as_view(), name='insumo_delete'),

    #Enlace
    path('enlace/', EnlaceListView.as_view(), name='enlace_list'),
    path('nuevo_enlace/', EnlaceCreateView.as_view(), name='enlace_create'),
    path('boletadetalle<int:pk>/', BoletaDetailView.as_view(), name='boleta_detail'), 
    path('editar_enlace/<int:pk>/', EnlaceUpdateView.as_view(), name='enlace_update'),
    path('eliminar_enlace/<int:pk>/', EnlaceDeleteView.as_view(), name='enlace_delete'),

    #Boletas
    path('boletas/', BoletaListView.as_view(), name='boleta_list'),
    path('boletas/nuevo/', BoletaCreateView.as_view(), name='boleta_create'),
    path('boletas/editar/<int:pk>/', BoletaUpdateView.as_view(), name='boleta_edit'),
    path('boletas/eliminar/<int:pk>/', BoletaDeleteView.as_view(), name='boleta_delete'),

    #Calendario
    path('cuentas/calendario/', views.calendario, name='calendario'),

    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
    path('exportar_tramitacion_excel/', views.exportar_tramitacion_excel, name='exportar_tramitacion_excel'),


    # Pagos de Clientes
    path('pagos-cliente/', PagoClienteListView.as_view(), name='pago_cliente_list'),
    path('pagos-cliente/nuevo/', PagoClienteCreateView.as_view(), name='pago_cliente_create'),
    path('pagos-cliente/<int:pk>/', PagoClienteDetailView.as_view(), name='pago_cliente_detail'),
    path('pagos-cliente/<int:pk>/editar/', PagoClienteUpdateView.as_view(), name='pago_cliente_edit'),
    path('pagos-cliente/<int:pk>/eliminar/', PagoClienteDeleteView.as_view(), name='pago_cliente_delete'),
    # Detalles de Pago
    path('pagos-cliente/<int:pago_id>/agregar-pago/', crear_detalle_pago, name='crear_detalle_pago'),
    path('detalle-pago/<int:detalle_id>/editar/', editar_detalle_pago, name='editar_detalle_pago'),
    path('detalle-pago/<int:detalle_id>/eliminar/', eliminar_detalle_pago, name='eliminar_detalle_pago'),

    # Reportes
    path('pagos-cliente/reporte/', reporte_pagos_cliente, name='reporte_pagos_cliente'),

]
