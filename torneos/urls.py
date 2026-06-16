from django.urls import path
from . import views

urlpatterns = [
    # 1. Página de inicio / Home de la app
    path('', views.index, name='index'),
    
    # 2. Pantalla con la cartelera de torneos
    path('lista/', views.lista_torneos, name='lista_torneos'),
    
    # 3. Ruta para procesar la inscripción (recibe el ID dinámico del torneo)
    path('inscribir/<int:torneo_id>/', views.inscribir_a_torneo, name='inscribir_a_torneo'),
]