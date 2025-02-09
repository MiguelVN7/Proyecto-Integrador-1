from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):  # Extendemos el modelo de usuario de Django
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    GENEROS = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    genero = models.CharField(max_length=1, choices=GENEROS, default='M')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    


