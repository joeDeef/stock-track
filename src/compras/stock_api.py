# acciones/stock_api.py
from datetime import datetime, timedelta
import yfinance as yf

class StockAPI:
    @staticmethod
    def obtener_precio_accion_actual(accion):
        """
        Obtiene el precio actual de la acción.
        """
        stock = yf.Ticker(accion)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return price

    @staticmethod
    def obtener_precio_accion_en_fecha(accion, fecha):
        """
        Obtiene el precio de la acción en una fecha específica.
        """
        stock = yf.Ticker(accion)
        fecha_fin = datetime.strptime(fecha, '%Y-%m-%d') + timedelta(days=1)
        fecha_fin = fecha_fin.strftime('%Y-%m-%d')
        datos_historicos = stock.history(start=fecha, end=fecha_fin)

        if not datos_historicos.empty:
            precio = datos_historicos["Close"].iloc[-1]
            return precio
        else:
            raise Exception(f"No hay datos disponibles para {accion} en la fecha {fecha}.")
        
    @staticmethod
    def obtener_nombre_empresa(ticker):
        """
        Obtiene el nombre de la empresa de un ticker utilizando la API de Yahoo Finance.
        """
        stock = yf.Ticker(ticker)
        info = stock.info
        nombre_empresa = info.get('shortName', 'No disponible')
        return nombre_empresa