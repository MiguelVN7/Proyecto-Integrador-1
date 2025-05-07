# LandingPage/forms.py
from django import forms
from django.contrib.auth import get_user_model
from .models import Reserva

Usuario = get_user_model()

class DatosPersonalesForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'segundo_nombre', 'last_name', 'segundo_apellido',
                  'email', 'fecha_nacimiento', 'genero', 'numero_estudiante', 'carrera', 'semestre', 'facultad', 'codigo']
        
class DatosUniversitariosForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['numero_estudiante', 'carrera', 'semestre', 'facultad', 'codigo']

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['espacio', 'fecha', 'hora', 'desea_suplementos']