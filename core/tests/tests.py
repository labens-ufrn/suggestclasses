import os
import django
from django.contrib.auth.models import User

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

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


class SugestaoTurmaTests(TestCase):

    def setUp(self):
        criar_dados()

    def tearDown(self):
        remover_dados()

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
            print(docente)

        print(ComponenteCurricular.objects.all())

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
