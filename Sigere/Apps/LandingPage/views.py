from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.conf import settings
from openai import OpenAI
from .models import Reserva, Usuario, EspacioDeportivo
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import DatosPersonalesForm, DatosUniversitariosForm
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm
from django.contrib import messages

client = OpenAI(api_key=settings.OPENAI_API_KEY)


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

def reservar(request):
    """Vista para la página de reservas."""
    return render(request, 'LandingPage/reservar.html')

@login_required
def misReservas(request):
    reservas_usuario = Reserva.objects.filter(usuario=request.user).order_by('-fecha', '-hora')
    return render(request, 'LandingPage/misReservas.html', {
        'reservas': reservas_usuario
    })


"""
def deportivos_view(request):
    # Obtiene la lista de deportes únicos
    deportes = EspacioDeportivo.objects.values_list('deporte', flat=True).distinct()
    # Serializa todos los espacios para usarlos en JS
    espacios_qs = EspacioDeportivo.objects.all().values('id', 'nombre', 'deporte')
    espacios_json = json.dumps(list(espacios_qs))
    
    return render(request, 'LandingPage/deportivos.html', {
        'deportes': deportes,
        'espacios_json': espacios_json,
    })
"""

def calendario_view(request):
    return render(request, 'LandingPage/calendario.html')


@login_required
def perfil_view(request):
    usuario = request.user

    if request.method == 'POST':
        if 'guardar_personales' in request.POST:
            form_personal = DatosPersonalesForm(request.POST, instance=usuario)
            form_uni = DatosUniversitariosForm(instance=usuario)  # solo carga, no guarda
            if form_personal.is_valid():
                form_personal.save()
                messages.success(request, "Datos personales actualizados.")
                return redirect('LandingPage:perfil')

        elif 'guardar_universitarios' in request.POST:
            form_uni = DatosUniversitariosForm(request.POST, instance=usuario)
            form_personal = DatosPersonalesForm(instance=usuario)  # solo carga, no guarda
            if form_uni.is_valid():
                form_uni.save()
                messages.success(request, "Datos universitarios actualizados.")
                return redirect('LandingPage:perfil')
    else:
        form_personal = DatosPersonalesForm(instance=usuario)
        form_uni = DatosUniversitariosForm(instance=usuario)

    return render(request, 'LandingPage/perfil.html', {
        'form_personal': form_personal,
        'form_uni': form_uni,
        'total_reservas': usuario.total_reservas(),
        'reservas_activas': usuario.reservas_activas(),
        'reservas_pasadas': usuario.reservas_pasadas(),
        'reservas_canceladas': usuario.reservas_canceladas(),
    })

def reservado_view(request):
    return render(request, 'LandingPage/reservado.html')


"""
def reservar_deportivos(request):
    # Obtiene la lista de deportes únicos
    deportes = EspacioDeportivo.objects.values_list('deporte', flat=True).distinct()
    # Serializa todos los espacios para usarlos en JS
    espacios_qs = EspacioDeportivo.objects.all().values('id', 'nombre', 'deporte')
    # Puedes usar json.dumps o el helper de Django
    import json
    espacios_json = json.dumps(list(espacios_qs))
    
    return render(request, 'deportivos.html', {
        'deportes': deportes,
        'espacios_json': espacios_json,
    }) 
    """

@login_required
def reservar_deportivos(request):
    deportes = EspacioDeportivo.objects.values_list('deporte', flat=True).distinct()
    espacios_qs = EspacioDeportivo.objects.all().values('id', 'nombre', 'deporte')
    espacios_json = json.dumps(list(espacios_qs))

    if request.method == 'POST':
        espacio_id = request.POST.get('espacio')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        desea_suplementos = request.POST.get('desea_suplementos') == 'on'

        espacio = EspacioDeportivo.objects.get(id=espacio_id)

        Reserva.objects.create(
            usuario=request.user,  # ⚠️ Esta parte es crucial
            espacio=espacio,
            fecha=fecha,
            hora=hora,
            desea_suplementos=desea_suplementos
        )

        return redirect('LandingPage:reservado')
    else:
        form = ReservaForm()

    return render(request, 'LandingPage/deportivos.html', {
        'deportes': deportes,
        'espacios_json': espacios_json,
        'form': form,
    })






# Ia, generación de descripción de espacio deportivo e imagen

def descripcion_espacio_deportivo(request):
    if 'nombre' not in request.GET:
        return JsonResponse({'error': 'Debe proporcionar el nombre del espacio'}, status=400)

    nombre_espacio = request.GET['nombre']

    try:
        respuesta = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente que describe espacios deportivos universitarios."},
            {"role": "user", "content": f"Describe brevemente el espacio deportivo llamado '{nombre_espacio}' que puede ser reservado por estudiantes en una universidad."}
        ],
        max_tokens=100,
        temperature=0.7)
        descripcion = respuesta.choices[0].message.content.strip()
        return JsonResponse({'descripcion': descripcion})
    except Exception as e:
        return JsonResponse({'error': f'Ocurrió un error al generar la descripción: {str(e)}'}, status=500)

def generar_imagen_espacio(request):
    if 'nombre' not in request.GET:
        return JsonResponse({'error': 'Debe proporcionar el nombre del espacio'}, status=400)

    nombre_espacio = request.GET['nombre']

    try:
        respuesta = openai.images.generate(
            model="dall-e-3",
            prompt=f"Ilustración digital de un espacio deportivo universitario llamado '{nombre_espacio}', moderno y bien iluminado",
            size="1024x1024",
            n=1
        )
        imagen_url = respuesta.data[0].url
        return JsonResponse({'imagen_url': imagen_url})
    except Exception as e:
        return JsonResponse({'error': f'Ocurrió un error al generar la imagen: {str(e)}'}, status=500)

@csrf_exempt
def descripcion_e_imagen_view(request):
    descripcion = None
    imagen_url = None

    if request.method == 'POST':
        nombre_espacio = request.POST.get('nombre')
        generar_imagen = request.POST.get('generar_imagen') == 'on'

        try:
            respuesta = client.chat.completions.create(model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente que describe espacios deportivos universitarios."},
                {"role": "user", "content": f"Describe en aproximadamente 100 palabras el espacio deportivo llamado '{nombre_espacio}' que puede ser reservado por estudiantes en una universidad."}
            ],
            max_tokens=150,
            temperature=0.7)
            descripcion = respuesta.choices[0].message.content.strip()
        except Exception as e:
            descripcion = f"Error generando descripción: {str(e)}"

        if generar_imagen:
            try:
                response_img = client.images.generate(
                    model="dall-e-3",
                    prompt=f"Ilustración digital de un espacio deportivo universitario llamado '{nombre_espacio}', moderno y bien iluminado",
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                imagen_url = response_img.data[0].url
            except Exception as e:
                imagen_url = f"Error generando imagen: {str(e)}"

        # Guardar en la base de datos si se generó correctamente
        espacio, creado = EspacioDeportivo.objects.get_or_create(nombre=nombre_espacio)
        if descripcion and not descripcion.startswith("Error"):
            espacio.descripcion = descripcion
        if imagen_url and not imagen_url.startswith("Error"):
            espacio.imagen_url = imagen_url
        espacio.save()

    return render(request, 'LandingPage/descripcion_imagen.html', {
        'descripcion': descripcion,
        'imagen_url': imagen_url
    })
