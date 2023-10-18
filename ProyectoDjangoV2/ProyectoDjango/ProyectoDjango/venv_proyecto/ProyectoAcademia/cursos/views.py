from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Curso, AsignacionAlumnoCurso
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usuario.models import UsuarioAlumno
from django.http import FileResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def cursos_ver(request):
    cursos = Curso.objects.filter(disponibilidad=True)

    return render(request, "cursos/cursos_ver.html", {"cursos": cursos})

def cursos(request):
    usuario = request.user
    asignaciones = AsignacionAlumnoCurso.objects.filter(alumno=usuario)
    cursos_asignados = [asignacion.curso for asignacion in asignaciones]

    cursos_no_asignados = Curso.objects.filter(disponibilidad=True).exclude(id__in=[curso.id for curso in cursos_asignados])

    return render(request, "cursos/cursos.html", {"cursos_asignados": cursos_asignados, "cursos_no_asignados": cursos_no_asignados})

def seleccionado(request, curso_id):
    curso=Curso.objects.get(id=curso_id)

    return render(request,"cursos/seleccionado.html", {"curso":curso})

def asignar_curso(request, curso_id, user_id):

    alumno = get_object_or_404(User, pk=user_id)
    curso = get_object_or_404(Curso, pk=curso_id)

    asignacion_existente = AsignacionAlumnoCurso.objects.filter(alumno=alumno, curso=curso).exists()

    if not asignacion_existente:
        asignacion = AsignacionAlumnoCurso(alumno=alumno, curso=curso, nombre_alumno=alumno.username, nombre_curso=curso.nombre)
        asignacion.save()

    cursos=Curso.objects.all()
    usuario = request.user 
    asignaciones = AsignacionAlumnoCurso.objects.filter(alumno=usuario)
    cursos_asignados = [asignacion.curso for asignacion in asignaciones]
    cursos_no_asignados = [curso for curso in cursos if curso not in cursos_asignados]

    return render(request,"cursos/cursos.html", {"cursos_asignados": cursos_asignados, "cursos_no_asignados": cursos_no_asignados})

def desasignar_curso(request, curso_id, user_id):

    alumno = get_object_or_404(User, pk=user_id)
    curso = get_object_or_404(Curso, pk=curso_id)

    asignacion = get_object_or_404(AsignacionAlumnoCurso, alumno=alumno, curso=curso)

    asignacion.delete()

    cursos=Curso.objects.all()
    usuario = request.user 
    asignaciones = AsignacionAlumnoCurso.objects.filter(alumno=usuario)
    cursos_asignados = [asignacion.curso for asignacion in asignaciones]
    cursos_no_asignados = [curso for curso in cursos if curso not in cursos_asignados]

    return render(request,"cursos/cursos.html", {"cursos_asignados": cursos_asignados, "cursos_no_asignados": cursos_no_asignados})

@login_required
def enviar_cursos(request):
    usuario = request.user

    asignaciones = AsignacionAlumnoCurso.objects.filter(alumno=usuario)

    cursos_info = "\n".join([f"{asignacion.curso.nombre}" for asignacion in asignaciones])
    mensaje = f"Tus cursos asignados son:\n{cursos_info}"

    try:
        usuario_alumno = UsuarioAlumno.objects.get(user=usuario)
        correo_destino = usuario_alumno.email
    except UsuarioAlumno.DoesNotExist:
        correo_destino = usuario.email

    send_mail('Tus cursos asignados', mensaje, 'tu_correo@gmail.com', [correo_destino])

    return redirect('Home') 

def generar_certificado_pdf(request):
    usuario = request.user

    cursos_aprobados = AsignacionAlumnoCurso.objects.filter(alumno=usuario, nota__gte=61.0)

    buffer = BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Certificado de Cursos Aprobados")
    y = 730  

    for asignacion in cursos_aprobados:
        curso = asignacion.curso
        nota = asignacion.nota
        texto = f"{curso.nombre} - Nota: {nota}"
        c.drawString(100, y, texto)
        y -= 20 

    c.showPage()
    c.save()
    buffer.seek(0)

    response = FileResponse(buffer, as_attachment=True, filename='certificado.pdf')
    return response