import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from core.bo.curriculo import get_curriculo_by_cc
from core.models import ComponenteCurricular
from core.tests.povoar_testes import criar_dados, remover_dados
from django.test import TestCase


class CurriculoTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nCurriculoTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_get_curriculo_by_cc(self):
        componente = ComponenteCurricular.objects.get(id_componente=99999)
        curriculos = get_curriculo_by_cc(componente.id_componente)

        self.assertIsNotNone(curriculos, 'Curriculos 1 não é None?')
        self.assertEqual(1, len(curriculos), 'Testando quantidade de currículos 1.')

        componente = ComponenteCurricular.objects.get(id_componente=99998)
        curriculos = get_curriculo_by_cc(componente.id_componente)

        self.assertIsNotNone(curriculos, 'Curriculos 2 não é None?')
        self.assertEqual(2, len(curriculos), 'Testando quantidade de currículos 2.')
