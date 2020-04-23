import django
django.setup()
from django.test import TestCase, Client
from django.urls import reverse
from core.models import EstruturaCurricular


class EstruturaCurricularTests(TestCase):

    def test_create_estrutura(self):
        """
                Teste de Unidade em Python.
        """
        bsi = EstruturaCurricular(codigo='01A', nome='SISTEMAS DE INFORMAÇÃO - Presencial - MT')

        self.assertEqual('01A', bsi.codigo, 'Testando sigla')

    def test_view(self):
        client = Client()
        response = client.get(reverse('horarios_list'))

        self.assertEqual(200, response.status_code, 'Testando View list_horarios')
