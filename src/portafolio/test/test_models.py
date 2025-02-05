from django.test import TestCase
from usuarios.models import UsuarioPersonalizado
from portafolio.models import Portafolio
from compras.models import Accion
from datetime import date

class PortafolioModelTest(TestCase):

    def setUp(self):
        """ Configuración inicial con usuario, portafolio y acciones de prueba """
        self.usuario = UsuarioPersonalizado.objects.create(
            email="usuario@test.com",
            nombres="Juan",
            apellidos="Pérez"
        )
        self.portafolio = Portafolio.objects.create(usuario=self.usuario)

        # Creación de acciones con diferentes precios y cantidades
        self.accion1 = Accion.objects.create(
            portafolio=self.portafolio,
            nombre="EmpresaX",
            cantidad=10,
            precio_compra=100.0,
            fecha_compra=date(2024, 1, 1),
            precio_actual=120.0
        )
        self.accion2 = Accion.objects.create(
            portafolio=self.portafolio,
            nombre="EmpresaY",
            cantidad=5,
            precio_compra=200.0,
            fecha_compra=date(2024, 2, 1),
            precio_actual=150.0
        )

    def test_obtener_acciones_exito(self):
        """ Caso de éxito: Obtener acciones cuando el portafolio tiene acciones """
        acciones = self.portafolio.obtener_acciones()
        self.assertEqual(len(acciones), 2)  # Debe haber 2 acciones

    def test_obtener_acciones_fallo(self):
        """ Caso de fallo: Obtener acciones cuando el portafolio está vacío """
        # Crear un usuario nuevo para evitar el error de unicidad
        usuario_vacio = UsuarioPersonalizado.objects.create(
            username="usuario_vacio_unique",  # Ensure this is unique
            email="usuario_vacio@test.com",
            nombres="Carlos",
            apellidos="Lopez"
        )
        portafolio_vacio = Portafolio.objects.create(usuario=usuario_vacio)
        acciones = portafolio_vacio.obtener_acciones()
        self.assertEqual(len(acciones), 0)  # No debe haber acciones
