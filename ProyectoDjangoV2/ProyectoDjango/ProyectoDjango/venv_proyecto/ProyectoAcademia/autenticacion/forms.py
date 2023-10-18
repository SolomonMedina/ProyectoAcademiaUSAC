from django import forms
from usuario.models import UsuarioAlumno

class FormularioUsuario(forms.ModelForm):
    class Meta:
        model = UsuarioAlumno
        fields = ('nombre','apellido','dpi','fecha_nacimiento','telefono','email','imagen')
       