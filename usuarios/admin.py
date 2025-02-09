from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

# Register your models here.

class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('segundo_nombre', 'fecha_nacimiento', 'genero'),
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)

