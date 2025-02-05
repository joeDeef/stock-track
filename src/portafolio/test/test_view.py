from django.test import TestCase
from django.contrib.auth import get_user_model
from usuarios.models import UsuarioPersonalizado
from portafolio.models import Portafolio
from compras.models import Accion

class TestPortafolioConsolidacionView(TestCase):
    
    def setUp(self):
        # Crear un usuario personalizado
        self.user = UsuarioPersonalizado.objects.create_user(
            username='testuser',
            password='testpassword',
            nombres='Test User',
        )
        
        # Crear un portafolio asociado al usuario
        self.portafolio = Portafolio.objects.create(usuario=self.user)
        
        # Crear algunas acciones y asociarlas con el portafolio
        self.accion1 = Accion.objects.create(nombre="Accion 1", cantidad=10, precio_compra=100.0, precio_actual=110.0, portafolio=self.portafolio)
        self.accion2 = Accion.objects.create(nombre="Accion 2", cantidad=20, precio_compra=50.0, precio_actual=60.0, portafolio=self.portafolio)
    
    def test_get_portafolio_y_consolidacion(self):
        # Verificar que el portafolio existe
        response = self.client.get('/ruta_a_tu_vista/')
        
        self.assertEqual(response.status_code, 200)
        
        # Verificar que las acciones y consolidación están presentes en el contexto
        self.assertIn('acciones_portafolio', response.context)
        self.assertIn('acciones_consolidadas', response.context)
        
        # Verificar la consolidación
        consolidado = response.context['acciones_consolidadas']
        self.assertEqual(len(consolidado), 2)  # Debe haber dos acciones consolidadas
        self.assertEqual(consolidado[0]['nombre'], "Accion 1")
        self.assertEqual(consolidado[1]['nombre'], "Accion 2")
    
    def test_get_portafolio_sin_acciones(self):
        # Crear un portafolio sin acciones
        portafolio_vacio = Portafolio.objects.create(usuario=self.user)
        
        # Verificar que el portafolio vacío muestra el mensaje correspondiente
        response = self.client.get('/ruta_a_tu_vista/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('mensaje', response.context)
        self.assertEqual(response.context['mensaje'], 'No tienes un portafolio aún.')
