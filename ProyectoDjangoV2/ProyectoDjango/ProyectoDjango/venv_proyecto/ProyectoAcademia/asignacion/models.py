from django.db import models
from django.contrib.auth import get_user_model
from cursos.models import Curso
from django.db.models import F, Sum, FloatField

User=get_user_model()

class Asignacion(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    created_at=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.id
    
    @property
    def total(self):
        return self.asignacioncurso_set.aggregate(
            total=Sum(F("precio"),output_field=FloatField())
        )["total"]

    class Meta:
        db_table='asignaciones'
        verbose_name='asignacion'
        verbose_name_plural='asignaciones'
        ordering=['id']

class AsignacionCurso(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    curso=models.ForeignKey(Curso, on_delete=models.CASCADE)
    asignacion=models.ForeignKey(Asignacion, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    #def __str__(self):
       # return f'{self.user} asignado el curso {self.curso_id.nombre}'
    
    class Meta:
        db_table='asignacioncursos'
        verbose_name='Asignación Curso'
        verbose_name_plural='Asignaciones Cursos'
        ordering=['id']
