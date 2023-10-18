from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import VRegistro,cerrar_sesion,iniciar_sesion,reconocimiento_facial

urlpatterns = [
    path('', VRegistro.as_view(), name="Autenticacion"),
    path('cerrar_sesion', cerrar_sesion, name="Cerrar_sesion"),
    path('iniciar_sesion', iniciar_sesion, name="Iniciar_sesion"),
    path('reconocimiento_facial', reconocimiento_facial, name='reconocimiento_facial'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
