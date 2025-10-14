from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from .models import Reserva, Usuario, EspacioDeportivo, PerfilUniversitario, Resena
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, FormView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
import json
from .forms import DatosPersonalesForm, DatosUniversitariosForm
from django.contrib.auth.decorators import login_required
from .forms import ReservaForm, ResenaForm

from Sigere.Apps.LandingPage.services import (
    get_ai_provider,
    AIProviderError,
    get_pending_reservations_for_review,
    get_review_stats_for_space,
    get_top_rated_spaces,
)


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
        numero_estudiante = request.POST.get('numero_estudiante')
        carrera = request.POST.get('carrera')
        semestre = request.POST.get('semestre')
        facultad = request.POST.get('facultad')
        codigo = request.POST.get('codigo')

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

            # Crear/Ajustar perfil universitario normalizado
            perfil_universitario, _ = PerfilUniversitario.objects.get_or_create(usuario=user)
            perfil_universitario.numero_estudiante = numero_estudiante
            perfil_universitario.carrera = carrera
            perfil_universitario.semestre = semestre
            perfil_universitario.facultad = facultad
            perfil_universitario.codigo = codigo
            perfil_universitario.save()

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

class MisReservasView(LoginRequiredMixin, ListView):
    template_name = 'LandingPage/misReservas.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        return (Reserva.objects
                .for_user(self.request.user)
                .ordered_recent_first())


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


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'LandingPage/perfil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        perfil, _ = PerfilUniversitario.objects.get_or_create(usuario=usuario)
        context.setdefault('form_personal', DatosPersonalesForm(instance=usuario))
        context.setdefault('form_uni', DatosUniversitariosForm(instance=perfil))
        context.update({
            'total_reservas': usuario.total_reservas(),
            'reservas_activas': usuario.reservas_activas(),
            'reservas_pasadas': usuario.reservas_pasadas(),
            'reservas_canceladas': usuario.reservas_canceladas(),
        })
        return context

    def post(self, request, *args, **kwargs):
        usuario = request.user
        perfil, _ = PerfilUniversitario.objects.get_or_create(usuario=usuario)
        form_personal = DatosPersonalesForm(instance=usuario)
        form_uni = DatosUniversitariosForm(instance=perfil)

        if 'guardar_personales' in request.POST:
            form_personal = DatosPersonalesForm(request.POST, instance=usuario)
            if form_personal.is_valid():
                form_personal.save()
                messages.success(request, "Datos personales actualizados.")
                return redirect('LandingPage:perfil')

        elif 'guardar_universitarios' in request.POST:
            form_uni = DatosUniversitariosForm(request.POST, instance=perfil)
            if form_uni.is_valid():
                form_uni.save()
                messages.success(request, "Datos universitarios actualizados.")
                return redirect('LandingPage:perfil')

        context = self.get_context_data(form_personal=form_personal, form_uni=form_uni)
        return self.render_to_response(context)


class ReviewDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'LandingPage/resenas_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        context.update({
            'pending_reservations': get_pending_reservations_for_review(usuario),
            'mis_resenas': Resena.objects.for_user(usuario).ordered_recent_first(),
            'top_spaces': get_top_rated_spaces(),
        })
        return context


class ReviewCreateView(LoginRequiredMixin, FormView):
    template_name = 'LandingPage/resena_form.html'
    form_class = ResenaForm
    success_url = reverse_lazy('LandingPage:resenas_dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.reserva = get_object_or_404(
            Reserva,
            pk=self.kwargs['reserva_id'],
            usuario=request.user,
            cancelada=False,
        )
        if self.reserva.fecha > timezone.now().date():
            messages.error(request, 'Solo puedes calificar reservas ya realizadas.')
            return redirect('LandingPage:resenas_dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'usuario': self.request.user,
            'reserva': self.reserva,
        })
        return kwargs

    def form_valid(self, form):
        Resena.objects.create(
            usuario=self.request.user,
            espacio=self.reserva.espacio,
            reserva=self.reserva,
            calificacion=form.cleaned_data['calificacion'],
            comentario=form.cleaned_data.get('comentario', ''),
        )
        messages.success(self.request, '¡Gracias por calificar el espacio!')
        return super().form_valid(form)


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Resena
    template_name = 'LandingPage/resena_confirm_delete.html'
    success_url = reverse_lazy('LandingPage:resenas_dashboard')

    def test_func(self):
        return self.get_object().usuario == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'La reseña fue eliminada correctamente.')
        return super().delete(request, *args, **kwargs)


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
        descripcion = get_ai_provider().generate_description(nombre_espacio, palabras=60)
        return JsonResponse({'descripcion': descripcion})
    except AIProviderError as exc:
        return JsonResponse({'error': str(exc)}, status=500)

def generar_imagen_espacio(request):
    if 'nombre' not in request.GET:
        return JsonResponse({'error': 'Debe proporcionar el nombre del espacio'}, status=400)

    nombre_espacio = request.GET['nombre']

    try:
        imagen_url = get_ai_provider().generate_image_url(nombre_espacio)
        return JsonResponse({'imagen_url': imagen_url})
    except AIProviderError as exc:
        return JsonResponse({'error': str(exc)}, status=500)

@csrf_exempt
def descripcion_e_imagen_view(request):
    descripcion = None
    imagen_url = None

    if request.method == 'POST':
        nombre_espacio = request.POST.get('nombre')
        generar_imagen = request.POST.get('generar_imagen') == 'on'
        provider = get_ai_provider()

        try:
            descripcion = provider.generate_description(nombre_espacio, palabras=100)
        except AIProviderError as exc:
            descripcion = f"Error generando descripción: {str(exc)}"

        if generar_imagen:
            try:
                imagen_url = provider.generate_image_url(nombre_espacio)
            except AIProviderError as exc:
                imagen_url = f"Error generando imagen: {str(exc)}"

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
