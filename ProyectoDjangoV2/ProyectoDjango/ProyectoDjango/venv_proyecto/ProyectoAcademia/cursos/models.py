from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class AreaCurso(models.Model):
    nombre=models.CharField(max_length=50)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

    class Meta:
        verbose_name="areaCurso"
        verbose_name_plural="areasCursos"

    def __str__(self):
        return self.nombre
    
class Curso(models.Model):
    nombre=models.CharField(max_length=50)
    descripcion=models.CharField(max_length=255)
    area=models.ForeignKey(AreaCurso, on_delete=models.CASCADE)
    imagen=models.ImageField(upload_to="cursos", null=True, blank=True)
    precio=models.FloatField(validators=[MinValueValidator(0.0)])
    alumnos = models.ManyToManyField(User, through='AsignacionAlumnoCurso')
    disponibilidad=models.BooleanField(default=True)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now_add=True)

    class Meta:
        verbose_name="Curso"
        verbose_name_plural="Cursos"

    def __str__(self):
        return self.nombre
    
class AsignacionAlumnoCurso(models.Model):
    nombre_alumno=models.CharField(max_length=50, default='default')
    nombre_curso=models.CharField(max_length=50, default='default')
    nota=models.FloatField(default=0.0)
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(auto_now_add=True)
    created=models.DateField(default=timezone.now)
    updated=models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('alumno', 'curso') 
        verbose_name="Asignación curso"
        verbose_name_plural="Asignaciones cursos"

    def __str__(self):
        return f"{self.alumno.username} asignado a {self.curso.nombre}"
