from core.bo.historico import criar_historico, excluir_historico, listar_historicos, listar_historicos_by_discente
from core.models import Historico
from core.dao.componente_dao import get_componente_by_id
from core.bo.discentes import get_discente_by_matricula
from core.tests.povoar_testes import criar_dados, remover_dados
from django.test import TestCase


class HistoricoTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nDiscenteTests')
        criar_dados()

    @classmethod
    def tearDownClass(self):
        super().tearDownClass()
        remover_dados()

    def test_add_historico(self):

        discente = get_discente_by_matricula(20209876543)
        componente = get_componente_by_id(id_componente=99999)

        self.assertIsNotNone(discente, 'Discente não é None?')
        self.assertEqual('20209876543', discente.matricula, 'Testando matricula discente')
        self.assertEqual('Zé Silva', discente.nome_discente, 'Testando nome discente')
        self.assertEqual('SISTEMAS DE INFORMAÇÃO', discente.nome_curso, 'Testando nome do curso')
        self.assertEqual('CENTRO DE  ENSINO SUPERIOR DO SERIDÓ', discente.nome_unidade, 'Testando nome unidade')

        self.assertEqual('DCT9999', componente.codigo, 'Testando código do componente')
        self.assertEqual('BANCO DE DADOS', componente.nome, 'Testando nome do ccomponente')

        historico = criar_historico(discente=discente, componente=componente)

        self.assertIsNotNone(historico, 'Histórico não é None?')
        self.assertIsNotNone(historico.pk, 'Histórico pk não é None?')
        self.assertEquals('20209876543', historico.discente.matricula, 'Recuperar matrícula do histórico')
        self.assertEquals('Zé Silva', historico.discente.nome_discente, 'Recuperar nome discente do histórico')
        self.assertEquals('DCT9999', historico.componente.codigo, 'Recuperar código componente do histórico')
        self.assertEquals('BANCO DE DADOS', historico.componente.nome, 'Recuperar nome componente do histórico')

        historicos = listar_historicos()
        print(historicos)
        self.assertEquals(1, len(historicos))
        
        historicos = listar_historicos_by_discente(discente=discente)
        print(historicos)
        self.assertEquals(1, len(historicos))


        excluir_historico(discente=discente, componente=componente)
        self.assertEquals(1, len(historicos))
