# LandingPage/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Reserva, PerfilUniversitario, Resena

Usuario = get_user_model()

class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'segundo_nombre', 'last_name', 'segundo_apellido',
                  'email', 'fecha_nacimiento', 'genero']
        
class DatosUniversitariosForm(forms.ModelForm):
    class Meta:
        model = PerfilUniversitario
        fields = ['numero_estudiante', 'carrera', 'semestre', 'facultad', 'codigo']

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['espacio', 'fecha', 'hora', 'desea_suplementos']


class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['calificacion', 'comentario']
        widgets = {
            'calificacion': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control', 'type': 'number'}),
            'comentario': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Comparte tu experiencia'})
        }

    def __init__(self, *args, usuario=None, reserva=None, **kwargs):
        self.usuario = usuario
        self.reserva = reserva
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.reserva is None or self.usuario is None:
            raise ValidationError('Debe seleccionar una reserva válida para calificar.')

        if self.reserva.usuario != self.usuario:
            raise ValidationError('Solo puedes calificar tus propias reservas.')

        if hasattr(self.reserva, 'resena') and not self.instance.pk:
            raise ValidationError('Esta reserva ya tiene una reseña registrada.')

        calificacion = cleaned_data.get('calificacion')
        if calificacion and not 1 <= calificacion <= 5:
            raise ValidationError('La calificación debe estar entre 1 y 5.')

        return cleaned_data