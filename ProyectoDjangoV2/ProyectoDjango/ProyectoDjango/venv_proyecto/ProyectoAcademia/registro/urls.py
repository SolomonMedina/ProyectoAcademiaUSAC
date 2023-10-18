from django.urls import path
from . import views

app_name="registro"

urlpatterns = [
    path("agregar/<int:curso_id>/",views.agregar_curso,name="agregar"),
    path("eliminar/<int:curso_id>/",views.eliminar_curso,name="eliminar"),
    path("limpiar/",views.darse_baja,name="limpiar"),
]

