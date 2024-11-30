from django.db import models
from datetime import datetime, timedelta
import yfinance as yf
from portafolio.models import Portafolio

class StockAPI:
    @staticmethod
    def obtener_precio_accion_actual(accion):
        stock = yf.Ticker(accion)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return price

    @staticmethod
    def obtener_precio_accion_en_fecha(accion, fecha):
        stock = yf.Ticker(accion)
        fecha_fin = datetime.strptime(fecha, '%Y-%m-%d') + timedelta(days=1)
        fecha_fin = fecha_fin.strftime('%Y-%m-%d')
        datos_historicos = stock.history(start=fecha, end=fecha_fin)

        if not datos_historicos.empty:
            precio = datos_historicos["Close"].iloc[-1]
            return precio
        else:
            raise Exception(f"No hay datos disponibles para {accion} en la fecha {fecha}.")

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