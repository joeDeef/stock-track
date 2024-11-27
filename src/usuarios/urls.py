from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.get_login, name='login'),
    path('signup/', views.get_signup, name='signup'),
    path('crearCuenta/', views.crear_cuenta, name='crearCuenta'),
    path('IniciarSesion/', views.iniciar_sesion, name='IniciarSesion'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),  # Redirigir al nombre de la URL 'inicio'
]
