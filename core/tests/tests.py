import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from dados import povoar
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
        response = client.get(reverse('list'))

        self.assertEqual(200, response.status_code, 'Testando View list_horarios')


class SugestaoTurmaTests(TestCase):

    def setUp(self):
        povoar.dados_testes()

    def test_create_sugestao(self):
        """
                        Teste de Unidade em Python.
        """
        codigo_turma = '01'
        siape = '1721652'
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
        local = Sala.objects.get(nome='Sala B1')
        ano = 2020
        periodo = 1
        descricao_horario = '56M12'
        capacidade_aluno = 25
        tipo = 'REGULAR'

        sugestao = SugestaoTurma(codigo_turma=codigo_turma, docente=docente,
                                 matricula_docente_externo=matricula_docente_externo, componente=cc,
                                 campus_turma=campus_turma, local=local, ano=ano, periodo=periodo,
                                 descricao_horario=descricao_horario, capacidade_aluno=capacidade_aluno, tipo=tipo)

        self.assertEqual('01', sugestao.codigo_turma, 'Código da Turma')
        self.assertEqual(1721652, sugestao.docente.siape, 'Matrícula Siape do Docente')
        self.assertEqual('', sugestao.matricula_docente_externo, 'Matrícula do Docente Externo')
