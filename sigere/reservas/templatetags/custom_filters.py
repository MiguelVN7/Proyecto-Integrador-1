from django import template

register = template.Library()

@register.filter
def filter_reserva(reservas, dia_hora):
    """
    Verifica si hay una reserva en el horario específico.
    reservas: Lista de objetos de reserva
    dia_hora: String en formato "Lunes:08:00"
    """
    dia, hora = dia_hora.split(":")  # Separar día y hora
    return any(reserva.dia == dia and reserva.hora == hora for reserva in reservas)
