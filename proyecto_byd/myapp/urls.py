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

# URLs AJAX para modales
path('api/listado/crear/', views.crear_listado_ajax, name='listado_crear_ajax'),
path('api/listado/editar/<int:pk>/', views.editar_listado_ajax, name='listado_editar_ajax'),
path('api/listado/eliminar/<int:pk>/', views.eliminar_listado_ajax, name='listado_eliminar_ajax'),

    #insumo
    path('insumo/', InsumosListView.as_view(), name='insumo_list'),  
    path('insumodetalle<int:pk>/', InsumosDetailView.as_view(), name='insumo_detail'),  
    path('insumocreate/', InsumosCreateView.as_view(), name='insumo_create'),  
    path('insumoupdate/<int:pk>/', InsumosUpdateView.as_view(), name='insumo_edit'),  
    path('insumodelete/<int:pk>/', InsumosDeleteView.as_view(), name='insumo_delete'),

    #Enlace
    path('enlace/', EnlaceListView.as_view(), name='enlace_list'),
    path('nuevo_enlace/', EnlaceCreateView.as_view(), name='enlace_create'),
    path('enlace/<int:pk>/', EnlaceDetailView.as_view(), name='enlace_detail'),
    path('editar_enlace/<int:pk>/', EnlaceUpdateView.as_view(), name='enlace_update'),
    path('eliminar_enlace/<int:pk>/', EnlaceDeleteView.as_view(), name='enlace_delete'),
    # URLs AJAX para enlaces
    path('api/enlace/crear/', views.crear_enlace_ajax, name='enlace_crear_ajax'),
    path('api/enlace/editar/<int:pk>/', views.editar_enlace_ajax, name='enlace_editar_ajax'),
    path('api/enlace/eliminar/<int:pk>/', views.eliminar_enlace_ajax, name='enlace_eliminar_ajax'),

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
    
    # API para actualizar notas de proyectos
    path('proyecto/<int:proyecto_id>/actualizar-notas/', actualizar_notas_proyecto, name='actualizar_notas_proyecto'),

    # APIs AJAX para sistema de pagos
    path('api/buscar-proyectos/', buscar_proyectos_ajax, name='buscar_proyectos_ajax'),
    path('api/proyecto/<int:proyecto_id>/datos/', obtener_datos_proyecto_ajax, name='obtener_datos_proyecto_ajax'),
    path('api/crear-pago-cliente/', crear_pago_cliente_ajax, name='crear_pago_cliente_ajax'),
    path('api/crear-detalle-pago/', crear_detalle_pago_ajax, name='crear_detalle_pago_ajax'),
    path('api/proyecto/<int:proyecto_id>/historial-pagos/', obtener_historial_pagos_ajax, name='obtener_historial_pagos_ajax'),
    
    # APIs AJAX para sistema dinámico
    path('api/pagos-clientes/', obtener_pagos_clientes_ajax, name='obtener_pagos_clientes_ajax'),
    path('api/pago-cliente/<int:pago_cliente_id>/info/', obtener_info_pago_cliente_ajax, name='obtener_info_pago_cliente_ajax'),
    path('api/pago-cliente/<int:pago_cliente_id>/detalles/', obtener_detalles_pago_cliente_ajax, name='obtener_detalles_pago_cliente_ajax'),
    
    # APIs AJAX para sistema de proyectos
    path('api/proyectos-con-pagos/', obtener_proyectos_con_pagos_ajax, name='obtener_proyectos_con_pagos_ajax'),
    path('api/proyecto/<int:proyecto_id>/info-completa/', obtener_info_proyecto_completa_ajax, name='obtener_info_proyecto_completa_ajax'),
    path('api/proyecto/<int:proyecto_id>/detalles-completos/', obtener_detalles_proyecto_completos_ajax, name='obtener_detalles_proyecto_completos_ajax'),
    
    # Sistema de pagos principal
    path('sistema-pagos/', sistema_pagos_view, name='sistema_pagos'),
    path('api/establecer-monto-total/', establecer_monto_total_ajax, name='establecer_monto_total_ajax'),
    path('api/recalcular-montos/', recalcular_montos_pagados, name='recalcular_montos_pagados'),

]
