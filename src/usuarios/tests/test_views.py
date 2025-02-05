from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

UsuarioPersonalizado = get_user_model()

class UsuariosViewsTest(TestCase):

    def setUp(self):
        """ Configuración inicial: crea un usuario de prueba """
        self.usuario = UsuarioPersonalizado.objects.create_user(
            username="usuario_test",
            password="clave_segura_123",
            nombres="Juan Pérez",
            telefono="0987654321",
            email="juanperez@example.com"
        )

    def test_get_login(self):
        """ Verifica que la página de login se carga correctamente """
        response = self.client.get(reverse('usuarios:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_iniciar_sesion_exitoso(self):
        """ Caso de éxito: usuario inicia sesión con credenciales correctas """
        response = self.client.post(reverse('usuarios:iniciarSesion'), {
            'email': 'juanperez@example.com',
            'password': 'clave_segura_123'
        })
        self.assertRedirects(response, '/registro/')  # Se espera redirección
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Inicio de sesión exitoso.')

    def test_iniciar_sesion_fallido(self):
        """ Caso de fallo: usuario intenta iniciar sesión con contraseña incorrecta """
        response = self.client.post(reverse('usuarios:iniciarSesion'), {
            'email': 'juanperez@example.com',
            'password': 'clave_incorrecta'
        })
        self.assertRedirects(response, reverse('usuarios:login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Correo electrónico o contraseña incorrectos.')

    def test_crear_cuenta_exitoso(self):
        """ Caso de éxito: se crea una cuenta correctamente """
        response = self.client.post(reverse('usuarios:crearCuenta'), {
            'nombre': 'Nuevo Usuario',
            'email': 'nuevo@example.com',
            'telefono': '0999999999',
            'password': 'clave_segura_456'
        })
        self.assertRedirects(response, reverse('usuarios:login'))
        self.assertTrue(UsuarioPersonalizado.objects.filter(email="nuevo@example.com").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Cuenta creada exitosamente.')

    def test_crear_cuenta_fallido(self):
        """ Caso de fallo: se intenta registrar con un email ya existente """
        response = self.client.post(reverse('usuarios:crearCuenta'), {
            'nombre': 'Usuario Duplicado',
            'email': 'juanperez@example.com',  # Email ya registrado
            'telefono': '0999999999',
            'password': 'clave_segura_789'
        })
        self.assertRedirects(response, reverse('usuarios:signup'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'El email ya está registrado.')

    def test_get_signup(self):
        """ Verifica que la página de registro se carga correctamente """
        response = self.client.get(reverse('usuarios:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registrar.html')

    def test_perfil_exitoso(self):
        """ Caso de éxito: usuario autenticado accede a su perfil """
        self.client.login(username='juanperez@example.com', password='clave_segura_123')
        response = self.client.get(reverse('usuarios:perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'perfil.html')

    def test_perfil_fallido(self):
        """ Caso de fallo: usuario no autenticado intenta acceder a perfil """
        response = self.client.get(reverse('usuarios:perfil'))
        self.assertEqual(response.status_code, 302)  # Se espera redirección al login

    def test_update_perfil_exitoso(self):
        """ Caso de éxito: usuario actualiza su perfil correctamente """
        self.client.login(username='juanperez@example.com', password='clave_segura_123')
        response = self.client.post(reverse('usuarios:updatePerfil'), {
            'nombre': 'Juan Actualizado',
            'email': 'juan_nuevo@example.com',
            'telefono': '0987654322',
            'contraseña_actual': 'clave_segura_123',
            'nueva_contraseña': 'nueva_clave_segura_456'
        })
        self.assertRedirects(response, reverse('usuarios:perfil'))
        self.usuario.refresh_from_db()
        self.assertEqual(self.usuario.nombres, 'Juan Actualizado')
        self.assertEqual(self.usuario.email, 'juan_nuevo@example.com')

    def test_update_perfil_fallido_contraseña_incorrecta(self):
        """ Caso de fallo: usuario intenta actualizar perfil con contraseña incorrecta """
        self.client.login(username='juanperez@example.com', password='clave_segura_123')
        response = self.client.post(reverse('usuarios:updatePerfil'), {
            'nombre': 'Juan Incorrecto',
            'email': 'juan_incorrecto@example.com',
            'telefono': '0987654323',
            'contraseña_actual': 'clave_erronea',
            'nueva_contraseña': 'nueva_clave'
        })
        self.assertRedirects(response, reverse('usuarios:perfil'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'La contraseña actual es incorrecta.')
