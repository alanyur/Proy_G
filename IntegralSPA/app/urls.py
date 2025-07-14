from django.urls import path
from .views import home, contacto, galeria, horario, sesion, registro, user_login, registro_succes, cerrar_sesion

urlpatterns = [
    path('', home, name='home'),
    path('contacto/<int:servicio_id>/', contacto, name='contacto'),
    path('galeria/',galeria,name='galeria'),
    path('horario/',horario, name='horario'),
    path('sesion/', user_login, name='sesion'),
    path('registro/', registro_succes, name='registro'),
    path('login/', user_login, name='login'),
    path('logout/', cerrar_sesion, name='logout'),
]
