from django.test import TestCase
from django.urls import reverse

class InicioViewsTest(TestCase):

    def test_get_inicio(self):
        """ Verifica que la página de inicio se carga correctamente """
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')