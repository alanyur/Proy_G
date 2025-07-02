from django.urls import path
from .views import home, contacto, galeria, horario, sesion, registro, user_login
urlpatterns = [
    path('', home, name='home'),
    path('contacto/',contacto,name='contacto'),
    path('galeria/',galeria,name='galeria'),
    path('horario/',horario, name='horario'),
    path('sesion/',sesion, name='sesion'),
    path('registro/',registro, name='registro'),
    path('login/', user_login, name='login'),
]
