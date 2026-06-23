from django.urls import path
from . import views

urlpatterns = [
    path('', views.resultados_torneos, name='resultados_torneos'),
    path('rendimiento/', views.rendimiento_jugadores, name='rendimiento_jugadores'),
    path('reportar/<str:username>/', views.reportar_usuario, name='reportar_usuario'),
]
