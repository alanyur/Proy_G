from django.urls import path
from .views import home, contacto, galeria, horario, sesion
urlpatterns = [
    path('', home, name='home'),
    path('contacto/',contacto,name='contacto'),
    path('galeria/',galeria,name='galeria'),
    path('horario/',horario, name='horario'),
    path('sesion/',sesion, name='sesion'),
]
