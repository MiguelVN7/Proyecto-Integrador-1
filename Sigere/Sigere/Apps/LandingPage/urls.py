from django.urls import path
from . import views

app_name = 'LandingPage'  # Esto es importante para usar namespaces como 'LandingPage:login'

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),  
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_page, name='home'),
]

