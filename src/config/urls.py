from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
import main, usuarios, compras, portafolio
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('nosotros/', include('nosotros.urls')),
    path('', include('main.urls'), name='home'),
    path('usuarios/', include('usuarios.urls')),
    path('registro/', include('compras.urls')),
    path('portafolio/', include('portafolio.urls')),
]