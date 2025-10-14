from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from django.core.exceptions import ValidationError

from .managers import ReservaQuerySet, ReviewQuerySet

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
    
    def total_reservas(self):
        return self.reserva_set.count()

    def reservas_activas(self):
        return self.reserva_set.active().count()

    def reservas_pasadas(self):
        return self.reserva_set.past().count()

    def reservas_canceladas(self):
        return self.reserva_set.cancelled().count()

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
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    total_resenas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.deporte})"
    
    def actualizar_metricas_resenas(self):
        resumen = self.resenas.aggregate(
            promedio=Avg('calificacion'),
            total=Count('id')
        )
        self.calificacion_promedio = (resumen['promedio'] or 0)
        self.total_resenas = resumen['total'] or 0
        self.save(update_fields=['calificacion_promedio', 'total_resenas'])


class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    espacio = models.ForeignKey(EspacioDeportivo, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    desea_suplementos = models.BooleanField(default=False)
    cancelada = models.BooleanField(default=False)

    objects = ReservaQuerySet.as_manager()

    def __str__(self):
        return f"{self.usuario.username} - {self.espacio.nombre} el {self.fecha} a las {self.hora}"


class PerfilUniversitario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil_universitario')
    numero_estudiante = models.CharField(max_length=35, blank=True, null=True)
    carrera = models.CharField(max_length=35, blank=True, null=True)
    semestre = models.CharField(max_length=35, blank=True, null=True)
    facultad = models.CharField(max_length=35, blank=True, null=True)
    codigo = models.CharField(max_length=35, blank=True, null=True)

    def __str__(self):
        return f"Perfil universitario de {self.usuario.username}"


@receiver(post_save, sender=Usuario)
def ensure_perfil_universitario(sender, instance, created, **kwargs):
    if created:
        PerfilUniversitario.objects.create(usuario=instance)


class Resena(TimeStampedModel):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='resenas')
    espacio = models.ForeignKey(EspacioDeportivo, on_delete=models.CASCADE, related_name='resenas')
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='resena')
    calificacion = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    publicada = models.BooleanField(default=True)

    objects = ReviewQuerySet.as_manager()

    class Meta:
        unique_together = ('usuario', 'espacio', 'reserva')
        ordering = ['-created_at']

    def __str__(self):
        return f"Reseña de {self.usuario.username} a {self.espacio.nombre}"

    def clean(self):
        if not 1 <= self.calificacion <= 5:
            raise ValidationError('La calificación debe estar entre 1 y 5.')


@receiver(post_save, sender=Resena)
def actualizar_metricas_resena(sender, instance, **kwargs):
    instance.espacio.actualizar_metricas_resenas()


@receiver(post_delete, sender=Resena)
def actualizar_metricas_resena_eliminada(sender, instance, **kwargs):
    instance.espacio.actualizar_metricas_resenas()