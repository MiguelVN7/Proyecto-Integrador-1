from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, EspacioDeportivo, Reserva

class UsuarioAdmin(UserAdmin):
    # Añade los campos personalizados a los campos de visualización
    list_display = ('username', 'email', 'first_name', 'segundo_nombre', 'last_name', 'segundo_apellido', 'is_staff')
    
    # Añade los campos personalizados a los campos de filtro
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {'fields': ('segundo_nombre', 'segundo_apellido', 'fecha_nacimiento', 'genero')}),
    )

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(EspacioDeportivo)
admin.site.register(Reserva)