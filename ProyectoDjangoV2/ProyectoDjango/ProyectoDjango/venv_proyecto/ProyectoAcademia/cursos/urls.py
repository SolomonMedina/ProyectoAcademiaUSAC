from django.urls import path
from . import views

urlpatterns = [
    path('',views.cursos, name="Cursos"),
    path('cursos_ver',views.cursos_ver, name="Cursos_Ver"),
    path('enviar_cursos',views.enviar_cursos, name="Enviar_Cursos"),
    path('seleccionado/<int:curso_id>/',views.seleccionado, name="Seleccionado"),
    path('asignar_curso/<int:curso_id>/<int:user_id>/',views.asignar_curso, name="Asignar_Curso"),
    path('desasignar_curso/<int:curso_id>/<int:user_id>/',views.desasignar_curso, name="Desasignar_Curso"),
    path('generar_certificado/',views.generar_certificado_pdf, name="generar_certificado"),
]

