from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('torneos/', views.lista_torneos, name='lista_torneos'),
    path('torneos/crear/', views.crear_torneo, name='crear_torneo'),
    path('torneos/<int:torneo_id>/', views.detalle_torneo, name='detalle_torneo'),
    path('torneos/<int:torneo_id>/inscribir/', views.inscribir_torneo, name='inscribir_torneo'),
    path('torneos/<int:torneo_id>/generar-bracket/', views.generar_bracket, name='generar_bracket'),
    path('torneos/<int:torneo_id>/bracket/', views.ver_bracket, name='ver_bracket'),
    path('torneos/<int:torneo_id>/desinscribir/', views.desinscribir_torneo, name='desinscribir_torneo'),
]