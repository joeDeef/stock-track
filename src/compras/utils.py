from .models import AccionDisponible

def obtener_detalles_acciones():
    """
    Obtiene el nombre de la empresa de todas las acciones disponibles
    desde la base de datos y las devuelve como una lista de diccionarios.
    """
    acciones_con_detalles = []

    for accion in AccionDisponible.objects.all():
        try:
            acciones_con_detalles.append({
                'nombre': accion.nombre_accion,
                'empresa': accion.empresa
            })
        except Exception as e:
            print(f"Error al obtener detalles de la acción {accion.nombre_accion}: {e}")
            acciones_con_detalles.append({
                'nombre': accion.nombre_accion,
                'empresa': 'No disponible'
            })
    
    return acciones_con_detalles
