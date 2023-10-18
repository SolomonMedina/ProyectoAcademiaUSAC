from django.shortcuts import render
from .models import UsuarioAlumno, UsuarioProfesor
from cursos.models import AsignacionAlumnoCurso, Curso

def usuario(request):

    usuario = request.user 
    datos_usuario = usuario.usuarioalumno
    asignaciones = AsignacionAlumnoCurso.objects.filter(alumno=usuario)
    cursos_asignados = [asignacion.curso for asignacion in asignaciones]
    
    return render(request,"usuario/usuario.html", {"cursos_asignados": cursos_asignados, "datos_usuario": datos_usuario, "asignaciones": asignaciones})

