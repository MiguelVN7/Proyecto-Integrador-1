from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    segundo_nombre = models.CharField(max_length=35, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=35, default='')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    GENEROS = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    genero = models.CharField(max_length=1, choices=GENEROS, default='M')
    
    # Estos campos ya vienen en AbstractUser:
    # - username
    # - email (correo)
    # - first_name (primer_nombre)
    # - last_name (puedes usar para primer_apellido)
    # - password
    
    def nombre_completo(self):
        cadena = "{0} {1}, {2} {3}"
        return cadena.format(self.last_name, self.segundo_apellido, self.first_name, self.segundo_nombre)

    def __str__(self):
        return self.nombre_completo()
    