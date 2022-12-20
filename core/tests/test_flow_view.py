import django
django.setup()
from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase, Client


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
        url = '/core/flow/bsi-1b-h/'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_flow_contabeis(self):
        client = Client()
        url = '/core/flow/cont/opcionais'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_flow_direito(self):
        client = Client()
        url = '/core/flow/dir/opcionais'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_flow_geo(self):
        client = Client()
        url = '/core/flow/geo-lic/opcionais'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_get_flow_mat(self):
        client = Client()
        url = '/core/flow/mat/opcionais'
        response = client.get(url)

        self.assertEqual(200, response.status_code)
