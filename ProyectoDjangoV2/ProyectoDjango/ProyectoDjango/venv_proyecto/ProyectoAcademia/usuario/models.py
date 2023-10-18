from django.db import models
from django.contrib.auth.models import User

class UsuarioAlumno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    dpi=models.IntegerField()
    fecha_nacimiento=models.CharField(max_length=10)
    telefono=models.IntegerField()
    email=models.EmailField(default="example@example.com")
    imagen=models.ImageField(upload_to="alumnos", null=True, blank=True)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

    class Meta:
        verbose_name="Usuario Alumno"
        verbose_name_plural="Usuarios Alumnos"

    def __str__(self):
        return self.nombre
        
    
class UsuarioProfesor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    username=models.CharField(max_length=50)
    nombre=models.CharField(max_length=50)
    apellido=models.CharField(max_length=50)
    dpi=models.IntegerField()
    imagen=models.ImageField(upload_to="profesores", null=True, blank=True)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

    class Meta:
        verbose_name="Usuario Profesor"
        verbose_name_plural="Usuarios Profesores"

    def __str__(self):
        return self.username
