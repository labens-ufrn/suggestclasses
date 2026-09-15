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

    def test_get_turmas_hist(self):
        client = Client()
        url = reverse('turmas_historia_lic')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_dir(self):
        client = Client()
        url = reverse('turmas_direito')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_mat(self):
        client = Client()
        url = reverse('turmas_matemática')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_his_bac(self):
        client = Client()
        url = reverse('turmas_historia_bac')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_geo_bac(self):
        client = Client()
        url = reverse('turmas_geografia_bac')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_geo_lic(self):
        client = Client()
        url = reverse('turmas_geografia_lic')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_ped(self):
        client = Client()
        url = reverse('turmas_pedagogia')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_adm(self):
        client = Client()
        url = reverse('turmas_administracao')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_let_esp(self):
        client = Client()
        url = reverse('turmas_letras_esp')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_let_pt(self):
        client = Client()
        url = reverse('turmas_letras_por')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_let_ing(self):
        client = Client()
        url = reverse('turmas_letras_ing')
        response = client.get(url)

        self.assertEqual(200, response.status_code)
