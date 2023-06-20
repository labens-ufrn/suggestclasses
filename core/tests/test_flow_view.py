import django
django.setup()
from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase, Client
from django.urls import reverse


class FlowViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nFlowViewTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_get_flow(self):
        client = Client()
        url = reverse('Fluxograma BSI - 01B - Horizontal')
        response = client.get(url)

        self.assertEqual(200, response.status_code)
