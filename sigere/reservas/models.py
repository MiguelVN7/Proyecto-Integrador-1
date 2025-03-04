from django.db import models
from django.contrib.auth.models import User  # Para vincular reservas a un usuario

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con Django Auth
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    universidad = models.CharField(max_length=150)
    carrera = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.universidad}"

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Relación con el usuario
    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.TextField()

    def __str__(self):
        return f"Reserva de {self.usuario.nombre} el {self.fecha} a las {self.hora}"
