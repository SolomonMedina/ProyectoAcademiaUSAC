from django.shortcuts import render
from django.shortcuts import redirect
from .registro import Registro
from cursos.models import Curso

def agregar_curso(request, curso_id):
    registro=Registro(request)
    curso=Curso.objects.get(id=curso_id)
    registro.agregar(curso=curso)
    return redirect("Cursos")

def eliminar_curso(request, curso_id):
    registro=Registro(request)
    curso=Curso.objects.get(id=curso_id)
    registro.eliminar(curso=curso)
    return redirect("Cursos")

def darse_baja(request, curso_id):
    registro=Registro(request)
    registro.borrar_todor()
    return redirect("Cursos")


