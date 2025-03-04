from django.shortcuts import render
from .models import Usuario, Reserva

def perfil_usuario(request):
    # Simulamos que el usuario ya está autenticado (más adelante usaremos autenticación real)
    usuario = Usuario.objects.first()  # Obtiene el primer usuario de la base de datos
    reservas = Reserva.objects.filter(usuario=usuario).order_by('fecha', 'hora')  # Ordena por fecha y hora

    return render(request, 'reservas/perfil.html', {'usuario': usuario, 'reservas': reservas})
