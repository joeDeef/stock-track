from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from compras.models import StockAPI, Accion
from django.http import JsonResponse
from django.template import TemplateDoesNotExist

def compras(request):
    try:
        acciones_disponibles = request.session.get('acciones_disponibles', [])
        return render(request, 'comprar.html', {'acciones_disponibles': acciones_disponibles})
    except TemplateDoesNotExist:
        return render(request, 'error.html', status=404)
    
@login_required
def comprar_accion(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cantidad = int(request.POST.get('cantidad'))
        precio_compra = float(request.POST.get('precio_accion'))
        fecha_compra = request.POST.get('fecha_compra')

        try:
            portafolio = request.user.portafolio
            StockAPI.obtener_precio_accion_actual(nombre)

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

            messages.success(request, f'Has registrado {cantidad} acción(es) de {nombre} en la fecha {fecha_compra} exitosamente.')
            return redirect('compras:comprar_accion')

        except Exception as e:
            messages.error(request, f'Error: No se pudo recuperar el precio de la acción. Por favor, inténtalo de nuevo.')
            return redirect('compras:comprar_accion')

    try:
        return render(request, 'comprar.html')
    except TemplateDoesNotExist:
        return render(request, 'error.html', status=404)
    
def obtener_precio_accion(request):
    fecha = request.GET.get("fecha")  # Fecha pasada en la URL, formato YYYY-MM-DD
    ticker = request.GET.get("nombre_accion")  # Ticker de la acción, puedes obtenerlo desde el request si es necesario

    # Usamos el método de StockAPI para obtener el precio de la acción en la fecha proporcionada
    try:
        precio = StockAPI.obtener_precio_accion_en_fecha(ticker, fecha)  # Ajusta esto a tu lógica
        return JsonResponse({"precio": precio})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)