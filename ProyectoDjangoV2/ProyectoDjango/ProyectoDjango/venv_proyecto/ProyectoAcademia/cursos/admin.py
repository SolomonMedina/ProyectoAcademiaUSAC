from django.contrib import admin
from .models import AreaCurso, Curso, AsignacionAlumnoCurso

class AreaCursoAdmin(admin.ModelAdmin):
    readonly_fields=("created","updated")

class CursoAdmin(admin.ModelAdmin):
    readonly_fields=("created","updated")

class AsignacionAlumnoCursoAdmin(admin.ModelAdmin):
    readonly_fields=("created","updated")

    readonly_fields = ('alumno', 'curso', 'fecha_asignacion', 'created', 'updated')
    list_display = ('nombre_alumno', 'nombre_curso', 'nota')

    def has_add_permission(self, request):
        return False

admin.site.register(AsignacionAlumnoCurso, AsignacionAlumnoCursoAdmin)
admin.site.register(AreaCurso, AreaCursoAdmin) 
admin.site.register(Curso, CursoAdmin)    

