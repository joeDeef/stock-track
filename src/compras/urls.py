# usuarios/urls.py
from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path('', views.compras, name='compras'),  
    path('comprar/', views.comprar_accion, name='comprar_accion'),
    path('api/precio_accion', views.obtener_precio_accion, name='obtener_precio_accion'),
]
