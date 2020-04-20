import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from django.contrib.auth.models import User
from core.tests.povoar_testes import criar_dados, remover_dados
from django.test import TestCase, Client
from django.urls import reverse
from core.models import EstruturaCurricular, ComponenteCurricular, SugestaoTurma, Docente, Departamento, Centro, Sala


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
