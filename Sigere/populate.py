import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sigere.settings')
django.setup()

from Sigere.Apps.LandingPage.models import EspacioDeportivo

espacios = [
    {"nombre": "Cancha sintética fútbol 7", "tipo_espacio": "cancha", "deporte": "Fútbol 7", "ubicacion": "Zona Norte"},
    {"nombre": "Cancha sintética de tenis de campo 1", "tipo_espacio": "cancha", "deporte": "Tenis de campo", "ubicacion": "Zona Norte"},
    {"nombre": "Cancha sintética de tenis de campo 2", "tipo_espacio": "cancha", "deporte": "Tenis de campo", "ubicacion": "Zona Norte"},
    {"nombre": "Cancha sintética de fútbolsala", "tipo_espacio": "cancha", "deporte": "Fútbol sala", "ubicacion": "Zona Sur"},
    {"nombre": "Cancha cubierta de baloncesto y voleibol", "tipo_espacio": "gimnasio", "deporte": "Baloncesto y Voleibol", "ubicacion": "Zona Deportiva Cubierta"},
    {"nombre": "Mesa de ping pong 1", "tipo_espacio": "mesa", "deporte": "Tenis de mesa", "ubicacion": "Zona Deportiva Cubierta"},
    {"nombre": "Mesa de ping pong 2", "tipo_espacio": "mesa", "deporte": "Tenis de mesa", "ubicacion": "Zona Deportiva Cubierta"},
    {"nombre": "Piscina", "tipo_espacio": "piscina", "deporte": "Natación", "ubicacion": "Complejo Acuático"},
    {"nombre": "Cancha de voleibol playa", "tipo_espacio": "cancha", "deporte": "Voleibol playa", "ubicacion": "Zona Arena"},
    {"nombre": "Cancha de balonmano", "tipo_espacio": "cancha", "deporte": "Balonmano", "ubicacion": "Zona Sur"},
    {"nombre": "Cancha múltiple cubierta", "tipo_espacio": "gimnasio", "deporte": "Multideporte", "ubicacion": "Zona Centro"},
    {"nombre": "Pista de atletismo", "tipo_espacio": "pista", "deporte": "Atletismo", "ubicacion": "Complejo Deportivo"},
    {"nombre": "Cancha de squash 1", "tipo_espacio": "cancha", "deporte": "Squash", "ubicacion": "Zona Indoor"},
    {"nombre": "Cancha de squash 2", "tipo_espacio": "cancha", "deporte": "Squash", "ubicacion": "Zona Indoor"},
    {"nombre": "Zona de calistenia", "tipo_espacio": "zona", "deporte": "Calistenia", "ubicacion": "Zona Verde"},
    {"nombre": "Sala de spinning", "tipo_espacio": "sala", "deporte": "Spinning", "ubicacion": "Bloque Fitness"},
    {"nombre": "Sala de yoga", "tipo_espacio": "sala", "deporte": "Yoga", "ubicacion": "Bloque Fitness"},
    {"nombre": "Salón de artes marciales", "tipo_espacio": "sala", "deporte": "Artes marciales", "ubicacion": "Bloque Deportivo"},
    {"nombre": "Zona de pesas", "tipo_espacio": "zona", "deporte": "Musculación", "ubicacion": "Gimnasio Principal"},
    {"nombre": "Cancha de béisbol", "tipo_espacio": "cancha", "deporte": "Béisbol", "ubicacion": "Zona Oeste"},
    {"nombre": "Cancha de padel", "tipo_espacio": "cancha", "deporte": "Padel", "ubicacion": "Zona Oeste"},

]

for espacio in espacios:
    EspacioDeportivo.objects.get_or_create(**espacio)

print("¡Espacios deportivos cargados correctamente!")