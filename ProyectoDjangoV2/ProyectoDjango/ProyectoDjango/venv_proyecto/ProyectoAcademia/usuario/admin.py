from django.contrib import admin
from .models import UsuarioProfesor, UsuarioAlumno

class UsuarioProfesorAdmin(admin.ModelAdmin):
    readonly_fields=("created","updated")

class UsuarioAlumnoAdmin(admin.ModelAdmin):
    readonly_fields=("created","updated")

admin.site.register(UsuarioProfesor, UsuarioProfesorAdmin) 
admin.site.register(UsuarioAlumno, UsuarioAlumnoAdmin)    