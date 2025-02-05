from django.test import TestCase
from unittest.mock import patch
from compras.models import Accion
from portafolio.models import Portafolio
from datetime import date

class AccionModelTest(TestCase):

    def setUp(self):
        """Crear datos de prueba"""
        # Suponiendo que Portafolio necesita fecha_creacion además de nombre
        self.portafolio = Portafolio.objects.create(
            nombre="Portafolio de Prueba", 
            fecha_creacion=date(2022, 1, 1)
        )
        self.accion = Accion.objects.create(
            portafolio=self.portafolio,
            nombre="AAPL",  # Nombre de la acción
            cantidad=10,
            precio_compra=100.0,
            fecha_compra=date(2023, 1, 1),
            precio_actual=100.0
        )

    def test_rendimiento_porcentaje(self):
        """Probar cálculo de rendimiento porcentual"""
        self.accion.precio_actual = 120.0
        self.assertEqual(self.accion.obtener_rendimiento_porcentaje(), 20.0)

    def test_rendimiento_dolares(self):
        """Probar cálculo de rendimiento en dólares"""
        self.accion.precio_actual = 120.0
        self.assertEqual(self.accion.obtener_rendimiento_dolares(), 200.0)

    @patch('acciones.models.StockAPI.obtener_precio_accion_actual', return_value=150.0)
    def test_actualizar_precio(self, mocked_api):
        """Probar actualización del precio llamando a la API mockeada"""
        self.accion.actualizar_precio()
        self.assertEqual(self.accion.precio_actual, 150.0)
        mocked_api.assert_called_once_with(self.accion.nombre)  # Verificamos que la API fue llamada correctamente
