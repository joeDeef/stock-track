from django.test import TestCase
from unittest.mock import patch
from compras.stock_api import StockAPI

class StockAPITest(TestCase):
    
    @patch('acciones.stock_api.yf.Ticker')
    def test_obtener_precio_accion_actual(self, MockTicker):
        """Probar la obtención del precio actual de una acción"""

        # Simular la respuesta del método history de yfinance
        mock_instance = MockTicker.return_value
        mock_instance.history.return_value = {
            "Close": [100.0]  # Simulamos que el precio de cierre es 100.0
        }

        # Llamar a la función que se quiere probar
        precio = StockAPI.obtener_precio_accion_actual('AAPL')

        # Comprobar que el precio devuelto es el que hemos simulado
        self.assertEqual(precio, 100.0)

    @patch('acciones.stock_api.yf.Ticker')
    def test_obtener_precio_accion_en_fecha(self, MockTicker):
        """Probar la obtención del precio de una acción en una fecha específica"""

        # Simular la respuesta del método history de yfinance
        mock_instance = MockTicker.return_value
        mock_instance.history.return_value = {
            "Close": [150.0]  # Simulamos que el precio de cierre en esa fecha es 150.0
        }

        # Llamar a la función que se quiere probar
        precio = StockAPI.obtener_precio_accion_en_fecha('AAPL', '2023-01-01')

        # Comprobar que el precio devuelto es el que hemos simulado
        self.assertEqual(precio, 150.0)

    @patch('acciones.stock_api.yf.Ticker')
    def test_obtener_nombre_empresa(self, MockTicker):
        """Probar la obtención del nombre de la empresa de un ticker"""

        # Simular la respuesta de info de yfinance
        mock_instance = MockTicker.return_value
        mock_instance.info = {'shortName': 'Apple Inc.'}

        # Llamar a la función que se quiere probar
        nombre_empresa = StockAPI.obtener_nombre_empresa('AAPL')

        # Comprobar que el nombre devuelto es el que hemos simulado
        self.assertEqual(nombre_empresa, 'Apple Inc.')

    @patch('acciones.stock_api.yf.Ticker')
    def test_obtener_precio_accion_en_fecha_no_disponible(self, MockTicker):
        """Probar que la excepción se lanza cuando no hay datos disponibles"""

        # Simular que no hay datos históricos disponibles
        mock_instance = MockTicker.return_value
        mock_instance.history.return_value = []

        # Llamar a la función y verificar que se lanza la excepción correcta
        with self.assertRaises(Exception):
            StockAPI.obtener_precio_accion_en_fecha('AAPL', '2023-01-01')
