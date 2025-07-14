from django.urls import path
from .views import home, contacto, galeria, horario, sesion, registro, user_login, registro_succes, cerrar_sesion

# Rutas url para la aplicacion
urlpatterns = [
    path('', home, name='home'), # pag principal
    path('contacto/<int:servicio_id>/', contacto, name='contacto'), # formulario
    path('galeria/',galeria,name='galeria'), # galeria de trabajps
    path('horario/',horario, name='horario'), # horario trabajadores
    path('sesion/', user_login, name='sesion'), # inicio de sesion
    path('registro/', registro_succes, name='registro'), # registro usuario
    path('login/', user_login, name='login'), # login
    path('logout/', cerrar_sesion, name='logout'), # logout
]
