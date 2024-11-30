from django.db import models
from usuarios.models import UsuarioPersonalizado

class Portafolio(models.Model):
    usuario = models.OneToOneField(
        UsuarioPersonalizado,
        on_delete=models.CASCADE,
        related_name="portafolio"
    )

    def __str__(self):
        return f"Portafolio de {self.usuario.nombres}"

    def obtener_acciones(self):
        return self.acciones.all()

    def obtener_rendimiento_porcentaje(self) -> float:
        acciones = self.acciones.all()
        rendimiento_total = sum(accion.obtener_rendimiento_dolares() for accion in acciones)
        inversion_total = sum(accion.precio_compra * accion.cantidad for accion in acciones)
        if inversion_total == 0:
            return 0.0
        return (rendimiento_total / inversion_total) * 100

    def obtener_rendimiento_dolares(self) -> float:
        return sum(accion.obtener_rendimiento_dolares() for accion in self.acciones.all())