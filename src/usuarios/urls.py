# usuarios/urls.py
from django.urls import path
from . import views

app_name = 'usuarios'  # Asegúrate de que esto esté presente

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('crearCuenta/', views.crear_cuenta, name='crearCuenta'),
    path('IniciarSesion/', views.iniciar_sesion, name='IniciarSesion'),
]
