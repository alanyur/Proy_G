from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Modelo de usuario con sus atributos
class Usuario(AbstractUser):
    ROLES = (
        ('cliente', 'Cliente'),
        ('trabajador', 'Trabajador'),
        ('admin', 'Administrador'),
    )

    telefono = models.CharField(max_length=20, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.username} ({self.rol})"

# Modelo de los posibles servicios a solicitar
class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo de una solicitud realizada por un cliente
class Solicitud(models.Model):
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'rol': 'cliente'})
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    descripcion = models.TextField()
    estado = models.CharField(max_length=30, default='pendiente')  # pendiente, aceptado, etc.
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud #{self.id} - {self.cliente.username}"

# Modelo para las calificaciones de los usuarios
class Calificacion(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField()

    def __str__(self):
        return f"{self.puntuacion}/5 - {self.solicitud}"

# Modelo para la disponibilidad de os trabajadores
class Disponibilidad(models.Model):
    trabajador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'rol': 'trabajador'})
    dia = models.CharField(max_length=10)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def __str__(self):
        return f"{self.trabajador.username} - {self.dia}"