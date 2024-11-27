# usuarios/urls.py
from django.urls import path
from . import views

app_name = 'usuarios'  # Asegúrate de que esto esté presente

urlpatterns = [
    path('', views.compras, name='compras'),
]
