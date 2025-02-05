from django.test import TestCase
from django.contrib.auth import get_user_model

UsuarioPersonalizado = get_user_model()

class UsuarioPersonalizadoTest(TestCase):

    def setUp(self):
        """ Configuración inicial de prueba """
        self.usuario = UsuarioPersonalizado.objects.create_user(
            username="usuario_test",
            password="clave_segura_123",
            nombres="Juan",
            apellidos="Pérez",
            telefono="0987654321",
            email="juanperez@example.com"
        )

    def test_creacion_usuario(self):
        """ Verifica que el usuario se creó correctamente """
        self.assertEqual(self.usuario.nombres, "Juan")
        self.assertEqual(self.usuario.apellidos, "Pérez")
        self.assertEqual(self.usuario.telefono, "0987654321")
        self.assertEqual(self.usuario.email, "juanperez@example.com")
        self.assertTrue(self.usuario.check_password("clave_segura_123"))

    def test_str_representacion(self):
        """ Verifica que __str__ devuelve el formato esperado """
        self.assertEqual(str(self.usuario), "Juan Pérez (usuario_test)")

    def test_creacion_superusuario(self):
        """ Verifica que se pueda crear un superusuario correctamente """
        admin_user = UsuarioPersonalizado.objects.create_superuser(
            username="admin_test",
            password="admin_clave_456",
            nombres="Admin",
            apellidos="Super",
            telefono="0999999999",
            email="admin@example.com"
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
