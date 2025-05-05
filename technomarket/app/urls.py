from django.urls import path
from .views import home, contacto, galeria, sobre_nosotros, horario
urlpatterns = [
    path('', home, name='home'),
    path('contacto/',contacto,name='contacto'),
    path('galeria/',galeria,name='galeria'),
    path('sobre-nosotros/',sobre_nosotros, name='sobre_nosotros'),
    path('horario/',horario, name='horario'),
]
