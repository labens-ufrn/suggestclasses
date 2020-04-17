import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from core.bo.docente import get_docente_by_siape, get_docente_by_nome
from core.tests.povoar_testes import criar_dados, remover_dados

from django.test import TestCase


class DocenteTests(TestCase):

    def setUp(self):
        criar_dados()

    def tearDown(self):
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
