import django
django.setup()

from unittest.case import TestCase

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from core.models import SugestaoTurma
from core.tests.povoar_testes import criar_dados, remover_dados


class SugestaoViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SugestaoViewTests, cls).setUpClass()
        print('\nSugestaoViewTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_sugestao_list(self):
        client = Client()
        response = client.get(reverse('sugestao_list'))

        self.assertEqual(200, response.status_code)

    def test_sugestao_detalhar(self):
        client = Client()
        sugestao = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999)

        url = reverse('sugestao_detalhar', args=(sugestao.pk,))
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_sugestao_editar(self):
        client = Client()
        sugestao = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999)

        url = reverse('sugestao_mat_editar', args=(sugestao.pk,))
        url2 = '/core/sugestao/mat/editar/' + sugestao.pk.__str__() + '/'
        response = client.get(url2)
        # self.assertEqual(403, response.status_code)
        self.assertEqual(302, response.status_code)

    def test_login_success(self):
        client = Client()
        user = User.objects.get(username='john')
        response = client.post('/core/usuario/logar', {'username': user.username, 'password': 'johnpassword'})
        self.assertEqual(response.url, '/core/')
        self.assertEqual(302, response.status_code)
