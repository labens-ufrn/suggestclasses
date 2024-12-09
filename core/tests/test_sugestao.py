import django
django.setup()
from django.contrib.auth.models import User

from core.bo.sugestao import solicitacao_incluir, solicitacao_existe, solicitacao_verificar_choques
from core.bo.sevices import get_estrutura_by_id
from core.bo.turma import get_sugestao_turmas, carrega_turmas_horario, carrega_sugestao_turmas, \
    converte_desc_horario
from core.models import SugestaoTurma, Curso, Docente, ComponenteCurricular, Sala

from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase


class SugestaoTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nSugestaoTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_get_sugestao(self):
        estrutura = get_estrutura_by_id(999999999)
        sugestao1 = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999)

        sugestao2 = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99998)

        sugestoes = get_sugestao_turmas(estrutura, semestre=1, ano=2020, periodo=2)

        self.assertIsNotNone(sugestoes, 'Sugestões não é None.')
        self.assertTrue(len(sugestoes) > 0, 'Testando qtd sugestões.')
        self.assertTrue(sugestao1 in sugestoes, 'Sugestão 1 pertente as sugestões!')
        self.assertTrue(sugestao2 in sugestoes, 'Sugestão 2 pertente as sugestões!')

    def test_criador_sugestao(self):
        criador_chefe = Docente.objects.get(siape=9999998)
        sugestao1 = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999)

        self.assertEqual(criador_chefe.usuario, sugestao1.criador, 'Verificando criador.')

    def test_carrega_turmas_horario(self):
        estrutura = get_estrutura_by_id(999999999)
        sugestao1 = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999)
        sugestoes = carrega_sugestao_turmas(estrutura, semestres=[1], ano=2020, periodo=2)

        horarios = converte_desc_horario(sugestao1.descricao_horario)

        turmas_por_horario = carrega_turmas_horario(sugestoes)

        # print(horarios[0])
        # print(turmas_por_horario[6][0])

        self.assertIsNotNone(turmas_por_horario, 'turmas_por_horario não é None.')

    def test_create_sugestao(self):
        """
                        Teste de Unidade em Python.
        """
        codigo_turma = '01'
        siape = '9999999'
        matricula_docente_externo = ''

        docente = None
        if siape != '' and Docente.objects.filter(siape=siape).exists():
            # Professores Substitutos e Temporários não estão na lista
            docente = Docente.objects.get(siape=siape)

        cc = ComponenteCurricular.objects.get(codigo='DCT9999')
        campus_turma = 'CERES - Caicó'
        local = Sala.objects.get(sigla='A01', bloco='Bloco A', centro__id_unidade=9999, campus=1)
        ano = 2020
        periodo = 1
        descricao_horario = '56M12'
        capacidade_aluno = 25
        tipo = 'REGULAR'
        total_solicitacoes = 0
        criador = User.objects.get(username='john')

        sugestao = SugestaoTurma(codigo_turma=codigo_turma, docente=docente,
                                 matricula_docente_externo=matricula_docente_externo, componente=cc,
                                 campus_turma=campus_turma, local=local, ano=ano, periodo=periodo,
                                 descricao_horario=descricao_horario, capacidade_aluno=capacidade_aluno,
                                 total_solicitacoes=total_solicitacoes, tipo=tipo, criador=criador)

        self.assertEqual('01', sugestao.codigo_turma, 'Código da Turma')
        self.assertEqual(9999999, sugestao.docente.siape, 'Matrícula Siape do Docente')
        self.assertEqual('', sugestao.matricula_docente_externo, 'Matrícula do Docente Externo')

    def test_incluir_solicitacao(self):
        """
            Teste para a inclusão de Solicitação de Turma por um discente.
        """
        componente1 = ComponenteCurricular.objects.get(id_componente=99999)
        sugestao = SugestaoTurma.objects.get(codigo_turma='01', componente=componente1, ano=2020, periodo=2)
        usuario = User.objects.get(username='discente1')
        discente = usuario.discente

        choque_comp, choque_horarios, houve_choques = \
            solicitacao_verificar_choques(discente, sugestao)
        self.assertIsNone(choque_comp)
        self.assertIsNone(choque_horarios)
        self.assertFalse(houve_choques)

        qtd1 = sugestao.solicitacaoturma_set.count()
        solicitacao, created = solicitacao_incluir(discente, sugestao)
        qtd2 = sugestao.solicitacaoturma_set.count()
        self.assertIsNotNone(solicitacao, 'Solicitação criada!')
        self.assertTrue(created, 'Solicitação criada!')
        self.assertEqual(qtd1 + 1, qtd2, 'Qtd Solicitações + 1.')

        resultado = solicitacao_existe(discente, sugestao)
        self.assertTrue(resultado, 'Solicitação do Discente existe!')

        qtd3 = sugestao.solicitacaoturma_set.count()
        solicitacao, created = solicitacao_incluir(discente, sugestao.pk)
        qtd4 = sugestao.solicitacaoturma_set.count()
        self.assertIsNotNone(solicitacao, 'Solicitação existe!')
        self.assertFalse(created, 'Solicitação não foi criada, já existia!')
        self.assertEqual(qtd3, qtd4, 'Qtd Solicitações não mudou.')

        solicitacao.delete()

        resultado = solicitacao_existe(discente, sugestao)
        self.assertFalse(resultado, 'Solicitação do Discente não existe!')

        qtd5 = sugestao.solicitacaoturma_set.count()
        self.assertEqual(qtd4 - 1, qtd5, 'Qtd Solicitações não mudou.')

    def test_choques_solicitacao(self):
        """
            Teste para a choques na inclusão de Solicitação de Turma por um discente.
        """
        componente1 = ComponenteCurricular.objects.get(id_componente=99999)
        componente3 = ComponenteCurricular.objects.get(id_componente=99997)
        sugestao1 = SugestaoTurma.objects.get(codigo_turma='01', componente=componente1, ano=2020, periodo=2)
        sugestao2 = SugestaoTurma.objects.get(codigo_turma='02', componente=componente1, ano=2020, periodo=2)
        sugestao3 = SugestaoTurma.objects.get(codigo_turma='01', componente=componente3, ano=2020, periodo=2)
        usuario = User.objects.get(username='discente1')
        discente = usuario.discente

        choque_comp, choque_horarios, houve_choques = \
            solicitacao_verificar_choques(discente, sugestao1)
        self.assertIsNone(choque_comp)
        self.assertIsNone(choque_horarios)
        self.assertFalse(houve_choques)

        solicitacao1, created = solicitacao_incluir(discente, sugestao1)

        # Não há choque, duas solicitações do mesmo componente em horários diferentes.
        choque_comp, choque_horarios, houve_choques = \
            solicitacao_verificar_choques(discente, sugestao2)
        self.assertIsNone(choque_comp)
        self.assertIsNone(choque_horarios)
        self.assertFalse(houve_choques)

        solicitacao2, created = solicitacao_incluir(discente, sugestao2)

        # Choque de Horários com outra solicitação de interesse.
        choque_comp, choque_horarios, houve_choques = \
            solicitacao_verificar_choques(discente, sugestao3)
        self.assertIsNotNone(choque_comp)
        self.assertIsNotNone(choque_horarios)
        self.assertTrue(houve_choques)

        solicitacao1.delete()
        solicitacao2.delete()
