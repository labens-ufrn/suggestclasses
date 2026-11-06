import django
django.setup()

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from core.models import Discente, SolicitacaoTurma, SugestaoTurma
from core.tests.povoar_testes import criar_dados


class SugestaoViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('\nSugestaoViewTests')
        criar_dados()
        cls.sugestao = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999)
        cls.john = User.objects.get(username='john')
        cls.discente = Discente.objects.get(matricula='20209876543')

    def test_sugestao_list(self):
        client = Client()
        response = client.get(reverse('sugestao_list'))

        self.assertEqual(200, response.status_code)

    def test_sugestao_detalhar(self):
        client = Client()
        url = reverse('sugestao_detalhar', args=(self.sugestao.pk,))
        response = client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.sugestao, response.context['object'])

    def test_sugestao_editar_sem_permissao_redireciona(self):
        """O handler403 do projeto converte a negação de permissão em 302 para '/'."""
        client = Client()
        url = reverse('sugestao_mat_editar', args=(self.sugestao.pk,))
        response = client.get(url)

        self.assertEqual(302, response.status_code)
        self.assertEqual('/', response.url)

    def test_login_success(self):
        client = Client()
        user = User.objects.get(username='john')
        url = reverse('Login de Usuário')
        index = reverse('index')
        response = client.post(url, {'username': user.username, 'password': 'johnpassword'})
        self.assertEqual(response.url, index)
        self.assertEqual(302, response.status_code)

    def test_solicitacao_listar(self):
        client = Client()
        client.force_login(self.john)
        solicitacao = SolicitacaoTurma.objects.create(
            usuario=self.john, solicitador=self.discente, turma=self.sugestao)

        url = reverse('solicitacao_turma_listar', args=(self.sugestao.pk,))
        response = client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'core/sugestao/solicitacao_listar.html')
        self.assertEqual(self.sugestao, response.context['turma'])
        self.assertEqual([solicitacao], list(response.context['solicitacoes']))

    def test_solicitacao_listar_anonimo_redireciona_para_login(self):
        url = reverse('solicitacao_turma_listar', args=(self.sugestao.pk,))
        response = Client().get(url)

        self.assertEqual(302, response.status_code)
        self.assertIn('/accounts/login', response.url)
