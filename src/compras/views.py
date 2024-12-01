from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from compras.models import StockAPI, Accion
from django.http import JsonResponse

def compras(request):
    acciones_disponibles = request.session.get('acciones_disponibles', [])
    return render(request, 'comprar.html', {'acciones_disponibles': acciones_disponibles})

@login_required
def comprar_accion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = int(request.POST.get('cantidad'))
        fecha_compra = request.POST.get('fecha_compra')  # Capturamos la fecha de compra

        if not nombre or cantidad <= 0:
            messages.error(request, 'Por favor, ingrese un nombre válido y una cantidad mayor a 0.')
            return redirect('compras:comprar_accion')

        if not fecha_compra:
            messages.error(request, 'Por favor, ingrese una fecha de compra válida.')
            return redirect('compras:comprar_accion')

        try:
            portafolio = request.user.portafolio
            precio_compra = StockAPI.obtener_precio_accion_en_fecha(nombre, fecha_compra)

            # Crear y guardar la nueva acción
            accion = Accion.objects.create(
                portafolio=portafolio,
                nombre=nombre,
                cantidad=cantidad,
                precio_compra=precio_compra,
                fecha_compra=fecha_compra 
            )

            # Actualizar el precio actual de la acción
            accion.actualizar_precio()

            messages.success(request, f'Has comprado {cantidad} acciones de {nombre} exitosamente.')
            return redirect('compras:comprar_accion')

        except Exception as e:
            messages.error(request, f'Error al comprar la acción: {str(e)}')
            return redirect('compras:comprar_accion')

    # Si no es un POST, renderiza el formulario
    return render(request, 'comprar.html')

def compras(request):
    acciones_disponibles = request.session.get('acciones_disponibles', [])
    return render(request, 'comprar.html', {'acciones_disponibles': acciones_disponibles})

def obtener_precio_accion(request):
    fecha = request.GET.get("fecha")  # Fecha pasada en la URL, formato YYYY-MM-DD
    ticker = request.GET.get("nombre_accion")  # Ticker de la acción, puedes obtenerlo desde el request si es necesario

    # Usamos el método de StockAPI para obtener el precio de la acción en la fecha proporcionada
    try:
        precio = StockAPI.obtener_precio_accion_en_fecha(ticker, fecha)  # Ajusta esto a tu lógica
        return JsonResponse({"precio": precio})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)