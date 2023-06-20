import django
django.setup()
from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase, Client
from django.urls import reverse


class TurmaViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nTurmaViewTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_get_flow(self):
        client = Client()
        url = reverse('turmas_sistemas')
        response = client.get(url)

        self.assertEqual(200, response.status_code)
