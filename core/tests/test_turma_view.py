import django
django.setup()
from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase, Client


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
        url = '/core/turmas/bsi'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_hist(self):
        client = Client()
        url = '/core/turmas/his-lic'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_dir(self):
        client = Client()
        url = '/core/turmas/dir'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_mat(self):
        client = Client()
        url = '/core/turmas/mat'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

