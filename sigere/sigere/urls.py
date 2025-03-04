from django.contrib import admin
from django.urls import path, include  # Asegúrate de importar 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservas/', include('reservas.urls')),  # Aquí conectamos las rutas de 'reservas'
]
