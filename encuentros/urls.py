from django.urls import path
from . import views

urlpatterns = [
    path('<int:encuentro_id>/cargar/', views.cargar_resultado, name='cargar_resultado'),
]