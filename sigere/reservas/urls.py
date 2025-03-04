from django.urls import path
from .views import perfil_usuario

urlpatterns = [
    path('perfil/', perfil_usuario, name='perfil'),
]



