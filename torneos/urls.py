from django.urls import path
from . import views

urlpatterns = [
    # ==========================================
    # RUTAS PÚBLICAS Y DE JUGADORES
    # ==========================================
    path('', views.index, name='index'),
    path('torneos/', views.lista_torneos, name='lista_torneos'),
    path('jugadores/', views.lista_jugadores, name='lista_jugadores'),
    path('torneos/crear/', views.crear_torneo, name='crear_torneo'),
    path('torneos/<int:torneo_id>/', views.detalle_torneo, name='detalle_torneo'),
    
    # ==========================================
    # GESTIÓN DE TORNEOS (INSCRIPCIONES Y BRACKETS)
    # ==========================================
    path('torneos/<int:torneo_id>/inscribir/', views.inscribir_torneo, name='inscribir_torneo'),
    path('torneos/<int:torneo_id>/desinscribir/', views.desinscribir_torneo, name='desinscribir_torneo'),
    path('torneos/<int:torneo_id>/generar-bracket/', views.generar_bracket, name='generar_bracket'),
    path('torneos/<int:torneo_id>/bracket/', views.ver_bracket, name='ver_bracket'),

    # ==========================================
    # PANEL DE ADMINISTRACION
    # ==========================================
    path('panel/', views.panel_admin, name='panel_admin'),
    path('panel/usuarios/', views.admin_usuarios, name='admin_usuarios'),
    path('panel/usuarios/<int:user_id>/banear/', views.admin_banear_usuario, name='admin_banear_usuario'),
    path('panel/usuarios/<int:user_id>/desbanear/', views.admin_desbanear_usuario, name='admin_desbanear_usuario'),
    path('panel/reportes/', views.admin_reportes, name='admin_reportes'),
    path('panel/reportes/<int:reporte_id>/resolver/', views.admin_resolver_reporte, name='admin_resolver_reporte'),
    path('panel/reportes/<int:reporte_id>/desestimar/', views.admin_desestimar_reporte, name='admin_desestimar_reporte'),
    path('panel/torneos/', views.admin_torneos, name='admin_torneos'),
    path('panel/torneos/<int:torneo_id>/editar/', views.admin_editar_torneo, name='admin_editar_torneo'),
    path('panel/torneos/<int:torneo_id>/cancelar/', views.admin_cancelar_torneo, name='admin_cancelar_torneo'),
]