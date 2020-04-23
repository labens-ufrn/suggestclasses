import django
django.setup()

from django.contrib.auth.models import Group
from core.bo.docente import get_docente_by_siape, get_docente_by_nome, get_funcao_by_siape
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
