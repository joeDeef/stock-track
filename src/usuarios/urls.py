from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.get_login, name='login'),
    path('signup/', views.get_signup, name='signup'),
    path('crearCuenta/', views.crear_cuenta, name='crearCuenta'),
    path('iniciarSesion/', views.iniciar_sesion, name='iniciarSesion'),
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('updatePerfil',views.update_perfil, name='updatePerfil')
]
