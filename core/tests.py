import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from django.test import TestCase, Client
from django.urls import reverse
from .models import EstruturaCurricular




class EstruturaCurricularTests(TestCase):

    def test_create_estrutura(self):
        """
                Teste de Unidade em Python.
        """
        bsi = EstruturaCurricular(sigla='01A', ano_periodo='2011.1', nome='SISTEMAS DE INFORMAÇÃO - Presencial - MT')

        self.assertEqual('01A', bsi.sigla, 'Testando sigla')

    def test_view(self):
        client = Client()
        response = client.get(reverse('list'))

        self.assertEqual(200, response.status_code, 'Testando View list_horarios')
