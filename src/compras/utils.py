from .stock_api import StockAPI
from .models import AccionDisponible

def obtener_detalles_acciones():
    """
    Obtiene el nombre de la empresa y el precio actual de todas las acciones disponibles
    desde la base de datos y las devuelve como una lista de diccionarios.
    """
    acciones_disponibles = AccionDisponible.objects.all()
    acciones_con_detalles = []

    for accion in acciones_disponibles:
        try:
            # Obtener precio y nombre de la empresa desde la API
            precio_actual = StockAPI.obtener_precio_accion_actual(accion.nombre_accion)
            nombre_empresa = StockAPI.obtener_nombre_empresa(accion.nombre_accion)
            
            acciones_con_detalles.append({
                'nombre': accion.nombre_accion,
                'precio_actual': precio_actual,
                'empresa': nombre_empresa
            })
        except Exception as e:
            print(f"Error al obtener detalles de la acción {accion.nombre_accion}: {e}")
            # En caso de error, puedes manejarlo como desees, por ejemplo:
            acciones_con_detalles.append({
                'nombre': accion.nombre_accion,
                'precio_actual': 'No disponible',
                'empresa': 'No disponible'
            })
    
    return acciones_con_detalles
