from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Usuario(AbstractUser):
    segundo_nombre = models.CharField(max_length=35, blank=True, null=True)
    segundo_apellido = models.CharField(max_length=35, default='')
    fecha_nacimiento = models.DateField(null=True, blank=True)
    GENEROS = [('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')]
    genero = models.CharField(max_length=1, choices=GENEROS, default='M')
    numero_estudiante = models.CharField(max_length=35, blank=True, null=True)
    carrera = models.CharField(max_length=35, blank=True, null=True)
    semestre = models.CharField(max_length=35, blank=True, null=True)
    facultad = models.CharField(max_length=35, blank=True, null=True)
    codigo = models.CharField(max_length=35, blank=True, null=True)

    
    # Estos campos ya vienen en AbstractUser:
    # - username
    # - email (correo)
    # - first_name (primer_nombre)
    # - last_name (puedes usar para primer_apellido)
    # - password
    
    def nombre_completo(self):
        cadena = "{0} {1}, {2} {3}"
        return cadena.format(self.last_name, self.segundo_apellido, self.first_name, self.segundo_nombre)
    
    def total_reservas(self):
        return self.reserva_set.count()

    def reservas_activas(self):
        return self.reserva_set.filter(fecha__gte=timezone.now().date()).count()

    def reservas_pasadas(self):
        return self.reserva_set.filter(fecha__lt=timezone.now().date()).count()

    def reservas_canceladas(self):
        return self.reserva_set.filter(cancelada=True).count()  # Solo si tienes un campo 'cancelada'

    def __str__(self):
        return self.nombre_completo()
    

class EspacioDeportivo(models.Model):
    TIPO_ESPACIO_CHOICES = [
        ('cancha', 'Cancha'),
        ('gimnasio', 'Gimnasio'),
        ('piscina', 'Piscina'),
        ('mesa', 'Mesa'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100, unique=True)
    tipo_espacio = models.CharField(max_length=20, choices=TIPO_ESPACIO_CHOICES)
    deporte = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=150)
    tiene_suplementos = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True)
    imagen_url = models.URLField(blank=True, null=True)  # para imagen generada por DALL·E

    def __str__(self):
        return f"{self.nombre} ({self.deporte})"
    

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    espacio = models.ForeignKey(EspacioDeportivo, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    desea_suplementos = models.BooleanField(default=False)
    cancelada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.espacio.nombre} el {self.fecha} a las {self.hora}"