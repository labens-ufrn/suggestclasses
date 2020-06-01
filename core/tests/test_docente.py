import django
django.setup()
from core.models import Horario
from django.contrib.auth.models import Group
from core.bo.docente import get_docente_by_siape, get_docente_by_nome, get_funcao_by_siape, carrega_turmas_por_horario, \
    get_vinculos_docente
from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase


class DocenteTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nDocenteTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_get_docentes(self):
        docente = get_docente_by_siape(9999999)

        self.assertIsNotNone(docente, 'Docente não é None?')
        self.assertEqual(9999999, docente.siape, 'Testando siape docente')
        self.assertEqual('Nome Docente Teste 1', docente.nome, 'Testando nome docente')
        self.assertEqual(9998, docente.id_unidade_lotacao, 'Testando id unidade de lotação docente')
        self.assertEqual('Departamento de Teste', docente.lotacao, 'Testando nome lotação docente')

        docente = get_docente_by_siape(8888888)
        self.assertIsNone(docente, 'Docente não é None?')

        docente = get_docente_by_siape('')
        self.assertIsNone(docente, 'Docente não é None?')

        docente = get_docente_by_nome('Nome Docente Teste 1')
        self.assertIsNotNone(docente, 'Docente não é None?')
        self.assertEqual(9999999, docente.siape, 'Testando siape docente')
        self.assertEqual('Nome Docente Teste 1', docente.nome, 'Testando nome docente')
        self.assertEqual(9998, docente.id_unidade_lotacao, 'Testando id unidade de lotação docente')
        self.assertEqual('Departamento de Teste', docente.lotacao, 'Testando nome lotação docente')

        docente = get_docente_by_nome('')
        self.assertIsNone(docente, 'Docente com nome vazio.')

        docente = get_docente_by_nome('Xuxa')
        self.assertIsNone(docente, 'Docente com nome que não existe.')

    def test_get_chefes(self):
        docente = get_docente_by_siape(9999998)
        funcoes = get_funcao_by_siape(9999998)
        chefe = None
        for fg in funcoes:
            if fg.atividade == 'CHEFE DE DEPARTAMENTO':
                chefe = fg

        self.assertTrue(len(funcoes) > 0, 'Testando funções')
        self.assertIsNotNone(chefe, 'Testando função chefe')
        self.assertEqual(chefe.siape, docente.siape)
        self.assertIsNotNone(chefe.nome, docente.nome)
        self.assertIsNotNone(chefe.id_unidade, docente.id_unidade_lotacao)
        grupo_chefes = Group.objects.get(name='ChefesTeste')
        grupos = docente.usuario.groups.all()
        self.assertTrue(grupo_chefes in grupos, 'Docente é chefe!')

        docente = get_docente_by_siape('')
        self.assertIsNone(docente, 'Docente com siape vazio.')

        funcoes = get_funcao_by_siape('')
        self.assertIsNone(docente, 'Docente com função vazio.')

    def test_get_vinculos(self):
        docente1 = get_docente_by_siape(9999999)
        docente2 = get_docente_by_siape(9999998)
        docente3 = get_docente_by_siape(9999997)
        horario = Horario.objects.get(dia=2, turno='T', ordem=3)

        vinculos1 = get_vinculos_docente(docente1, horario, 2020, 1)
        self.assertIsNotNone(vinculos1)
        self.assertEqual(len(vinculos1), 0, 'Não existe vinculos')

        vinculos2 = get_vinculos_docente(docente2, horario, 2020, 1)
        self.assertIsNotNone(vinculos2)
        self.assertEqual(len(vinculos2), 0, 'Não existe vinculos')

        vinculos3 = get_vinculos_docente(docente3, horario, 2020, 1)
        self.assertIsNotNone(vinculos3)
        self.assertEqual(len(vinculos3), 1, 'Existe vinculos')

        turmas1 = carrega_turmas_por_horario(docente1, 2020, 1)
        self.assertIsNotNone(turmas1, 'Existe turmas')
        turmas2 = carrega_turmas_por_horario(docente2, 2020, 1)
        self.assertIsNotNone(turmas2, 'Não Existe turmas'),
        turmas3 = carrega_turmas_por_horario(docente3, 2020, 1)
        self.assertIsNotNone(turmas3, 'Existe turmas')
