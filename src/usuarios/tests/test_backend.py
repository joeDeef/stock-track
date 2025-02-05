from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from usuarios.backends import EmailAuthBackend

UsuarioPersonalizado = get_user_model()

class EmailAuthBackendTest(TestCase):

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

    def test_autenticacion_exitosa(self):
        """ Verifica que un usuario pueda autenticarse con su email y contraseña correctos """
        user = authenticate(username="juanperez@example.com", password="clave_segura_123")
        self.assertIsNotNone(user)  # El usuario debería autenticarse correctamente
        self.assertEqual(user.email, "juanperez@example.com")

    def test_autenticacion_fallida(self):
        """ Verifica que no se pueda autenticar con un email incorrecto """
        user = authenticate(username="correo_inexistente@example.com", password="clave_segura_123")
        self.assertIsNone(user)  # No debería autenticarse porque el email no existe

    def test_autenticacion_contraseña_incorrecta(self):
        """ Verifica que no se pueda autenticar con una contraseña incorrecta """
        user = authenticate(username="juanperez@example.com", password="clave_incorrecta")
        self.assertIsNone(user)  # No debería autenticarse porque la contraseña es incorrecta
