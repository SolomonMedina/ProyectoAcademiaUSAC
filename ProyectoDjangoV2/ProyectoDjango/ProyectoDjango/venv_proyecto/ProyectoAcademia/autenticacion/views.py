from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout,authenticate, get_user_model
from django.contrib import messages
from .forms import FormularioUsuario
from usuario.models import UsuarioAlumno
from django import forms
import re
import cv2

from autenticacion.detection import FaceRecognition

faceRecognition = FaceRecognition()

class VRegistro(View):
    def get(self, request):
        form=CustomUserCreationForm()
        custom_form=FormularioUsuario()
        return render(request,"registro/registro.html",{"form":form,"custom_form":custom_form})
    
    def post(self,request):
        form=CustomUserCreationForm(request.POST)
        custom_form=FormularioUsuario(request.POST, request.FILES)
        if form.is_valid() and custom_form.is_valid():
            usuario=form.save()
            usuarioalumno = custom_form.save(commit=False)
            usuario.imagen = request.FILES['imagen']
            usuarioalumno.user = usuario
            usuarioalumno.save()
            addFace(request.POST['dpi'])
            login(request, usuario)
            return redirect('Home')
        else:
            for msg in form.error_messages:
                messages.error(request,form.error_messages[msg])
            
            return render(request,"registro/registro.html",{"form":form,"custom_form":custom_form})


def addFace(dpi):
    dpi = dpi
    faceRecognition.faceDetect(dpi)
    faceRecognition.trainFace()
    return redirect('/')


def cerrar_sesion(request):
    logout(request)
    return redirect('Home')

def iniciar_sesion(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            usuario=authenticate(username=username,password=password)
            
            if usuario is not None:
                login(request, usuario)
                return redirect('Home')
            else:
                messages.error(request,"Las credenciales ingresadas no coinciden con ningún usuario")
        else:
            messages.error(request,"Se ha ingresado información incorrecta")
            
    form=AuthenticationForm()
    return render(request,"login/login.html",{"form":form})

def reconocimiento_facial(request):
    face_id = faceRecognition.recognizeFace()  # Realiza el reconocimiento facial
    cam = cv2.VideoCapture(0)
    try:
        # Busca un usuario basado en el DPI en el modelo UsuarioAlumno
        usuarioalumno = UsuarioAlumno.objects.get(dpi=face_id)
        usuario = usuarioalumno.user

        if usuario is not None:
            login(request, usuario)
            return redirect('Home')
        else:
            messages.error(request, "Las credenciales ingresadas no coinciden con ningún usuario")

    except UsuarioAlumno.DoesNotExist:
        # Si no se encuentra el usuario, puedes redirigir a una página de error o mostrar un mensaje
        return redirect('PaginaDeError')  # Asegúrate de crear la vista y plantilla para la página de error

    # Detener la cámara y liberar los recursos
    cam.release()
    cv2.destroyAllWindows()


class CustomUserCreationForm(UserCreationForm):
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError("La contraseña debe contener al menos una mayúscula.")
        if not re.search(r'\d', password1):
            raise forms.ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[\W_]', password1):
            raise forms.ValidationError("La contraseña debe contener al menos un símbolo.")
        return password1
