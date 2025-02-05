from django.test import TestCase
from django.urls import reverse

class NosotrosViewsTest(TestCase):

    def test_get_nosotros(self):
        """ Verifica que la página de login se carga correctamente """
        response = self.client.get(reverse('nosotros:nosotros'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'nosotros.html')