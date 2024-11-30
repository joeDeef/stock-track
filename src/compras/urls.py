# usuarios/urls.py
from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path('', views.compras, name='compras'),  
    path('comprar/', views.comprar_accion, name='comprar_accion'),
]
