import django
django.setup()

from django.test import Client, TestCase
from django.urls import reverse

from core.tests.povoar_testes import criar_dados

# (nome da rota, status esperado)
ROTAS_TURMAS = [
    ('turmas_list', 200),
    ('turmas_contabeis', 200),
    ('turmas_direito', 200),
    ('turmas_geografia_bac', 200),
    ('turmas_geografia_lic', 200),
    ('turmas_historia_bac', 200),
    ('turmas_historia_lic', 200),
    ('turmas_matemática', 200),
    ('turmas_sistemas', 200),
    ('turmas_pedagogia', 200),
    ('turmas_administracao', 200),
    ('turmas_turismo', 200),
    ('turmas_letras_esp', 200),
    ('turmas_letras_por', 200),
    ('turmas_letras_ing', 200),
]


class TurmaViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('\nTurmaViewTests')
        criar_dados()

    def test_rotas_de_turmas(self):
        client = Client()

        for nome, status in ROTAS_TURMAS:
            with self.subTest(rota=nome):
                response = client.get(reverse(nome))

                self.assertEqual(status, response.status_code)
                if status == 200:
                    self.assertTrue(response.templates, 'a view não renderizou template')
