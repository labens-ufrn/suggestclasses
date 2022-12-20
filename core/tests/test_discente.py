import django
django.setup()
from core.bo.discentes import get_discentes, get_discente_by_matricula, get_discentes_ativos, get_qtd_discentes_ativos, get_discentes_by_centro
from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase


class DiscenteTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nDiscenteTests')
        criar_dados()

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        remover_dados()

    def test_get_discentes_by_matricula(self):
        discente = get_discente_by_matricula(20209876543)

        self.assertIsNotNone(discente, 'Discente não é None?')
        self.assertEqual('20209876543', discente.matricula, 'Testando matricula discente')
        self.assertEqual('Zé Silva', discente.nome_discente, 'Testando nome discente')
        self.assertEqual('SISTEMAS DE INFORMAÇÃO', discente.nome_curso, 'Testando nome do curso')
        self.assertEqual('CENTRO DE  ENSINO SUPERIOR DO SERIDÓ', discente.nome_unidade, 'Testando nome unidade')

    def test_get_discentes(self):
        discentes = get_discentes()

        self.assertIsNotNone(discentes, 'Discentes não é None?')
        self.assertTrue(len(discentes) > 0, 'Existe pelo menos um discente')

    def test_get_discentes_by_centro(self):
        pass

    def test_get_discentes_ativos(self):
        discentes = get_discentes_ativos()

        self.assertIsNotNone(discentes, 'Discentes não é None?')
        self.assertTrue(len(discentes) > 0, 'Existe pelo menos um discente')

    def test_get_qtd_discentes_ativos(self):
        discentes = get_qtd_discentes_ativos()

        self.assertIsNotNone(discentes, 'Quantidade de Discentes ativos não é None?')
