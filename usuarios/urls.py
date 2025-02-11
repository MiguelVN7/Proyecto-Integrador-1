from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import home, registro, iniciar_sesion, cerrar_sesion

urlpatterns = [
    path("login/", LoginView.as_view(template_name="usuarios/login.html"), name="login"),
    path("registro/", registro, name="registro"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),  
    path("", home, name="home"),
]


