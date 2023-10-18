from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from asignacion.models import Asignacion, AsignacionCurso
from django.contrib import messages
from registro.registro import Registro
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail

@login_required(login_url="/autenticacion/login")
def procesar_asignacion(request):
    asignacion=Asignacion.objects.create(user=request.user) #Asigna cursos a un usuario
    registro=Registro(request) #Conectado a lista de cursos, agrega/ elimina cursos
    asignacion_curso=list()
    for key, value in registro.registro.items():
        asignacion_curso.append(AsignacionCurso(
            curso_id=key,
            user=request.user,
            asignacion=asignacion
        ))
    AsignacionCurso.objects.bulk_create(asignacion_curso)
    enviar_correo(
        asignacion=asignacion,
        asignacion_curso=asignacion_curso,
        nombreusuario=request.user.username,
        emailusuario=request.user.email
    )
    messages.success(request, "Se han asignado sus cursos")
    return redirect("../cursos")

def enviar_correo(**kwargs):
    asunto="Se ha registrado su asignación"
    mensaje=render_to_string("emails/asignacion.html",{
        "asignacion":kwargs.get("asignacion"),
        "asignacion_curso":kwargs.get("asignacion_curso"),
        "nombreusuario":kwargs.get("nombreusuario")
    })
    mensaje_texto=strip_tags(mensaje)
    from_email="brianestrada.ab16@gmail.com"
    to=kwargs.get("emailusuario")

    send_mail(asunto,mensaje_texto,from_email,[to],html_message=mensaje)




