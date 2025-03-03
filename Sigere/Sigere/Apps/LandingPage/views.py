from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

def landing_page(request):
    """Vista para la página principal de bienvenida."""
    return render(request, 'LandingPage/landing.html')

def home_page(request):
    """Vista para la página principal."""
    return render(request, 'LandingPage/home.html')


def login_view(request):
    """Vista para la página de inicio de sesión."""
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Buscar el usuario por email
        try:
            user = Usuario.objects.get(email=email)
            # Usar authenticate con el username correcto
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user is not None:
                login(request, authenticated_user)
                messages.success(request, f"Bienvenido, {user.first_name}!")
                return redirect('LandingPage:home')
            else:
                messages.error(request, "Contraseña incorrecta.")
        except Usuario.DoesNotExist:
            messages.error(request, "No existe un usuario con ese correo electrónico.")
    
    # Si es GET o hubo error en POST, mostrar el formulario
    return render(request, 'LandingPage/login.html')


def signup_view(request):
    """Vista para la página de registro."""
    if request.method == 'POST':
        # Obtener los datos del formulario
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        password = request.POST.get('password')
        segundo_nombre = request.POST.get('segundo_nombre')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        last_name = request.POST.get('last_name')
        genero = request.POST.get('genero')
        segundo_apellido = request.POST.get('segundo_apellido')
        
        # Verificar si el correo ya existe
        if Usuario.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya está registrado.")
            return render(request, 'LandingPage/signup.html')
        
        try:
            # Crear el nuevo usuario
            user = Usuario(
                username = email.split("@")[0],  # Usamos el email como nombre de usuario
                email=email,
                first_name=first_name,
                last_name=last_name,
                segundo_nombre=segundo_nombre,
                segundo_apellido=segundo_apellido,
                fecha_nacimiento=fecha_nacimiento,
                genero=genero,
                password=make_password(password),  # Encriptamos la contraseña
                # Otros campos si son necesarios
            )
            user.save()
            
            # Iniciar sesión automáticamente después del registro
            login(request, user)
            
            messages.success(request, "Cuenta creada exitosamente.")
            return redirect('LandingPage:home')  # Redirigir a la página principal
            
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir
            messages.error(request, f"Error al crear la cuenta: {str(e)}")
    
    # Si es GET o hubo un error en POST, mostrar el formulario
    return render(request, 'LandingPage/signup.html')
