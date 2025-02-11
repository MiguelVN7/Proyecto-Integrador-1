from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # Inicia sesión automáticamente después de registrarse
            return redirect("/")  # O usa el name definido en urls.py

    else:
        form = RegistroForm()
    return render(request, "usuarios/registro.html", {"form": form})


def home(request):
    return render(request, "usuarios/home.html")  # Crea un template básico

def iniciar_sesion(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect("home")  # Redirige a la página principal después del login
    else:
        form = AuthenticationForm()
    
    return render(request, "usuarios/login.html", {"form": form})

def cerrar_sesion(request):
    logout(request)
    return redirect("/")
