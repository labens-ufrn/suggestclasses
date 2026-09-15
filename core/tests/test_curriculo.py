import django
django.setup()

from core.bo.curriculo import get_curriculo_by_cc, get_semestres_by_curso, get_componentes_by_curso,get_componentes_by_curso_semestre
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

    def test_get_semestres_by_curso(self):
        semestre = get_semestres_by_curso(9999)

        self.assertIsNotNone(semestre, 'Semestre 1 não é None?')
        self.assertEqual(0, len(semestre), 'Testando quantidade de currículos 1.')

    def test_get_componentes_by_curso(self):
        oc = get_componentes_by_curso(9999)

        self.assertIsNotNone(oc, 'Componentes por curso não é None?')
        self.assertEqual(0, len(oc), 'Testando quantidade de componentes.')

    def test_get_componentes_by_curso_semestre(self):
        pass
