from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Portafolio
from collections import defaultdict
from compras.models import Accion

@login_required
def get_portafolio(request):
    try:
        portafolio = request.user.portafolio
        acciones_portafolio = portafolio.obtener_acciones()

        for accion in acciones_portafolio:
            accion.actualizar_precio()
            accion.costo_total = round(accion.precio_compra * accion.cantidad, 2)
            accion.costo_mercado_total = round(accion.precio_actual * accion.cantidad, 2)

        return render(request, 'portafolio.html', {
            'acciones_portafolio': acciones_portafolio,
            'acciones_consolidadas' : get_consolidacion(portafolio)
        })
    except Portafolio.DoesNotExist:
        return render(request, 'portafolio.html', {
            'acciones_portafolio': [],
            'mensaje': 'No tienes un portafolio aún.',
        })

def get_consolidacion(portafolio):
    acciones_portafolio = portafolio.obtener_acciones()

    consolidated_accions = defaultdict(lambda: {'cantidad': 0, 'rendimiento_dolares': 0, 'precio_compra': 0})

    for accion in acciones_portafolio:
        consolidated_accions[accion.nombre]['cantidad'] += accion.cantidad
        consolidated_accions[accion.nombre]['rendimiento_dolares'] += accion.obtener_rendimiento_dolares()
        consolidated_accions[accion.nombre]['precio_compra'] += round(accion.precio_compra * accion.cantidad, 2)

    consolidated_list = []
    for nombre, data in consolidated_accions.items():
        consolidated_list.append({
            'nombre': nombre,
            'cantidad': data['cantidad'],
            'precio_compra': data['precio_compra'],
            'precio_costo': round(data['precio_compra'] / data['cantidad'] , 2),
            'rendimiento_dolares': data['rendimiento_dolares'],
            'rendimiento_porcentaje': round((data['rendimiento_dolares'] * 100) / data['precio_compra'] , 2)
        })

    return consolidated_list