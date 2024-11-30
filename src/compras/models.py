# acciones/models.py
from django.db import models
from .stock_api import StockAPI
from portafolio.models import Portafolio

class Accion(models.Model):
    portafolio = models.ForeignKey(
        Portafolio,
        on_delete=models.CASCADE,
        related_name="acciones"
    )
    nombre = models.CharField(max_length=50)
    cantidad = models.PositiveIntegerField()
    precio_compra = models.FloatField()
    fecha_compra = models.DateField()
    precio_actual = models.FloatField(default=0.0)

    def obtener_rendimiento_porcentaje(self) -> float:
        return ((self.precio_actual - self.precio_compra) / self.precio_compra) * 100

    def obtener_rendimiento_dolares(self) -> float:
        return (self.precio_actual - self.precio_compra) * self.cantidad

    def actualizar_precio(self):
        self.precio_actual = StockAPI.obtener_precio_accion_actual(self.nombre)
        self.save()

    def __str__(self):
        return f"{self.nombre} - {self.cantidad} acciones"

class AccionDisponible(models.Model):
    nombre_accion = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre_accion}"