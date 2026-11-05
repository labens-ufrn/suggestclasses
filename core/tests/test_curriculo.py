import django
django.setup()

from core.bo.curriculo import get_curriculo_by_cc, get_semestres_by_curso, get_componentes_by_curso, \
    get_componentes_by_curso_semestre
from core.models import ComponenteCurricular, Curso, EstruturaCurricular
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

    @staticmethod
    def _ativar_estrutura(id_curriculo):
        """As estruturas do povoamento são criadas sem status; ativa uma delas
        apenas no escopo da transação do teste."""
        estrutura = EstruturaCurricular.objects.get(id_curriculo=id_curriculo)
        estrutura.status = EstruturaCurricular.ATIVA
        estrutura.save()
        return estrutura

    def test_get_semestres_by_curso(self):
        curso = Curso.objects.get(codigo=9999)

        semestres = get_semestres_by_curso(curso)

        self.assertEqual([1, 2], list(semestres), 'Semestres do Curso Teste 1')

    def test_get_semestres_by_curso_sem_estrutura(self):
        curso_base = Curso.objects.get(codigo=9999)
        curso = Curso.objects.create(codigo=9990, nome='Curso Sem Estrutura', coordenador=curso_base.coordenador,
                                     nivel='Graduação', grau='Bacharelado', modalidade='Presencial',
                                     turno='Matutino', centro=curso_base.centro)

        semestres = get_semestres_by_curso(curso)

        self.assertEqual(0, len(semestres), 'Curso sem estrutura não tem semestres')

    def test_get_componentes_by_curso(self):
        curso = Curso.objects.get(codigo=9999)
        self._ativar_estrutura(999999999)

        componentes = get_componentes_by_curso(curso)

        self.assertEqual(['DCT9999', 'DCT9998', 'DCT9997'], [c.codigo for c in componentes],
                         'Componentes da estrutura ativa, ordenados por nome')

    def test_get_componentes_by_curso_sem_estrutura_ativa(self):
        curso = Curso.objects.get(codigo=9999)

        componentes = get_componentes_by_curso(curso)

        self.assertEqual(0, len(componentes), 'Estrutura inativa não deve retornar componentes')

    def test_get_componentes_by_curso_semestre(self):
        curso = Curso.objects.get(codigo=9999)
        self._ativar_estrutura(999999999)

        componentes = get_componentes_by_curso_semestre(curso, 1)

        self.assertEqual(['DCT9999', 'DCT9998'], [c.codigo for c in componentes],
                         'Componentes do semestre 1, ordenados por nome')

    def test_get_componentes_by_curso_semestre_sem_componentes(self):
        curso = Curso.objects.get(codigo=9999)
        self._ativar_estrutura(999999999)

        componentes = get_componentes_by_curso_semestre(curso, 3)

        self.assertEqual(0, len(componentes), 'Semestre 3 não tem componentes')
