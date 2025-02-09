from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm

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

