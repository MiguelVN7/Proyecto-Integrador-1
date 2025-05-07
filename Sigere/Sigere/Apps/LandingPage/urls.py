from django.urls import path
from . import views

app_name = 'LandingPage'  # Esto es importante para usar namespaces como 'LandingPage:login'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),  
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_page, name='home'),
    path('reservar/', views.reservar, name='reservar'),
    path('reservado/', views.reservado_view, name='reservado'),
    path('misReservas/', views.misReservas, name='misReservas'),
    path('deportivos/', views.reservar_deportivos, name='deportivos'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('descripcion-espacio/', views.descripcion_espacio_deportivo, name='descripcion_espacio'),
    path('generar-imagen/', views.generar_imagen_espacio, name='generar_imagen'),
    path('descripcion-e-imagen/', views.descripcion_e_imagen_view, name='descripcion_e_imagen'),

]

