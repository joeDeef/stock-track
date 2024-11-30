from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Portafolio

@login_required
def get_portafolio(request):
    try:
        portafolio = request.user.portafolio
        acciones_portafolio = portafolio.obtener_acciones()

        for accion in acciones_portafolio:
            accion.costo_total = round(accion.precio_compra * accion.cantidad, 2)
            accion.costo_mercado_total = round(accion.precio_actual * accion.cantidad, 2)

        return render(request, 'portafolio.html', {
            'acciones_portafolio': acciones_portafolio,
        })
    except Portafolio.DoesNotExist:
        return render(request, 'portafolio.html', {
            'acciones_portafolio': [],
            'mensaje': 'No tienes un portafolio aún.',
        })
