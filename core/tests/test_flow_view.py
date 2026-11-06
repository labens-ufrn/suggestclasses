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

    def test_get_flow_contabeis(self):
        client = Client()
        url = reverse('flow_cont_op')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_flow_direito(self):
        client = Client()
        url = reverse('flow_dir_op')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_flow_geo(self):
        client = Client()
        url = reverse('flow_geo_lic_op')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_flow_mat(self):
        client = Client()
        url = reverse('flow_mat_op')
        response = client.get(url)

        self.assertEqual(200, response.status_code)
