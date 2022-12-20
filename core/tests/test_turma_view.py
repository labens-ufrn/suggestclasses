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

    def test_get_turmas_his_bac(self):
        client = Client()
        url = '/core/turmas/his-bac'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_geo_bac(self):
        client = Client()
        url = '/core/turmas/geo-bac'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_geo_lic(self):
        client = Client()
        url = '/core/turmas/geo-lic'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_ped(self):
        client = Client()
        url = '/core/turmas/ped'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_adm(self):
        client = Client()
        url = '/core/turmas/adm'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_let_esp(self):
        client = Client()
        url = '/core/turmas/let-esp'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_let_pt(self):
        client = Client()
        url = '/core/turmas/let-por'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_turmas_let_ing(self):
        client = Client()
        url = '/core/turmas/let-ing'
        response = client.get(url)

        self.assertEqual(200, response.status_code)
