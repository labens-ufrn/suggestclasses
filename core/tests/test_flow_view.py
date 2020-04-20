import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase, Client


class FlowViewTests(TestCase):

    def setUp(self):
        print('FlowViewTests')
        criar_dados()

    def tearDown(self):
        remover_dados()

    def test_get_flow(self):
        client = Client()
        url = '/core/flow/bsi-1b-h/'
        response = client.get(url)

        self.assertEqual(200, response.status_code)
