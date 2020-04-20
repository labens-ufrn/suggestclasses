import django
from django.contrib.auth.models import User

from core.bo.sevices import get_estrutura_by_id
from core.bo.turma import get_sugestao_turmas, SugestaoTurmaEstendida, carrega_turmas_horario, carrega_sugestao_turmas, \
    converte_desc_horario
from core.models import SugestaoTurma, Curso, Docente, ComponenteCurricular, Sala

from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase


class SugestaoTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nSugestaoTests')
        django.setup()
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_get_sugestao(self):
        estrutura = get_estrutura_by_id(999999999)
        curso = Curso.objects.get(codigo=9999)
        sugestao1 = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999)
        sugestao_estendida1 = SugestaoTurmaEstendida(sugestao1, tipo_vinculo='OBRIGATÓRIO',
                                                     semestre=1, curso=curso)
        sugestao2 = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99998)
        sugestao_estendida2 = SugestaoTurmaEstendida(sugestao2, tipo_vinculo='OBRIGATÓRIO',
                                                     semestre=1, curso=curso)
        sugestoes = get_sugestao_turmas(estrutura, semestre=1, ano=2020, periodo=2)

        self.assertIsNotNone(sugestoes, 'Sugestões não é None.')
        self.assertTrue(len(sugestoes) > 0, 'Testando qtd sugestões.')
        self.assertTrue(sugestao_estendida1 in sugestoes, 'Sugestão 1 pertente as sugestões!')
        self.assertTrue(sugestao_estendida2 in sugestoes, 'Sugestão 2 pertente as sugestões!')

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
            # TODO Adicionar docente como foreign key de SugestaoTurma
            docente = Docente.objects.get(siape=siape)
            # print(docente)

        # print(ComponenteCurricular.objects.all())

        cc = ComponenteCurricular.objects.get(codigo='DCT9999')
        campus_turma = 'CERES - Caicó'
        local = Sala.objects.get(nome='Sala A01')
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
