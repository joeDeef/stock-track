from django.test import TestCase, Client
from django.contrib.auth.models import User
from compras.models import Accion
from unittest.mock import patch
from django.urls import reverse

class ComprarAccionTests(TestCase):
    def setUp(self):
        """ Configuración inicial antes de cada prueba """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')  # Simula un usuario autenticado

    @patch("compras.models.StockAPI.obtener_precio_accion_actual")
    def test_comprar_accion_exitoso(self, mock_stock_api):
        """ Prueba que comprar una acción funciona correctamente """
        mock_stock_api.return_value = 100.0  # Simulamos un precio de 100
        
        response = self.client.post(reverse('compras:comprar_accion'), {
            'nombre': 'AAPL',
            'cantidad': 5,
            'precio_accion': 100.0,
            'fecha_compra': '2024-02-01'
        })

        self.assertEqual(response.status_code, 302)  # Redirecciona después de comprar
        self.assertEqual(Accion.objects.count(), 1)  # Se debe haber creado una acción
        accion = Accion.objects.first()
        self.assertEqual(accion.nombre, 'AAPL')

    def test_comprar_accion_sin_autenticacion(self):
        """ Prueba que un usuario no autenticado no pueda comprar acciones """
        self.client.logout()
        response = self.client.post(reverse('compras:comprar_accion'), {
            'nombre': 'AAPL',
            'cantidad': 5,
            'precio_accion': 100.0,
            'fecha_compra': '2024-02-01'
        })
        self.assertEqual(response.status_code, 302)  # Django redirige a login

    @patch("compras.models.StockAPI.obtener_precio_accion_en_fecha")
    def test_obtener_precio_accion(self, mock_precio):
        """ Prueba la API que devuelve el precio de una acción en una fecha dada """
        mock_precio.return_value = 150.0

        response = self.client.get(reverse('compras:obtener_precio_accion'), {
            'nombre_accion': 'AAPL',
            'fecha': '2024-02-01'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"precio": 150.0})

    @patch("compras.models.StockAPI.obtener_precio_accion_en_fecha")
    def test_obtener_precio_accion_error(self, mock_precio):
        """ Prueba el manejo de errores cuando la API no encuentra un precio """
        mock_precio.side_effect = Exception("No hay datos disponibles")

        response = self.client.get(reverse('compras:obtener_precio_accion'), {
            'nombre_accion': 'AAPL',
            'fecha': '2024-02-01'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

