from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
import main, usuarios, compras

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('compras/', include('compras.urls')),
]
