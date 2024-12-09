import django
django.setup()

from unittest.case import TestCase

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from core.models import SugestaoTurma
from core.tests.povoar_testes import criar_dados, remover_dados

class SugestaoGeografiaViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(SugestaoGeografiaViewTests, cls).setUpClass()
        print('\nSugestaoGeografiaViewTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_sugestao_detalhar(self):
        client = Client()
        sugestao = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999)

        url = reverse('sugestao_detalhar', args=(sugestao.pk,))
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def sugestao_geo_bac_manter(self):
        client = Client()
        sugestao = SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999)

        url = reverse('sugestao_geo_bac_incluir', args=(sugestao.pk,))
        url2 = '/core/sugestao/geo-bac/incluir' + sugestao.pk.__str__() + '/'
        response = client.get(url2)
        self.assertEqual(302, response.status_code)

    def test_login_success(self):
        client = Client()
        user = User.objects.get(username='john')
        response = client.post('/core/usuario/logar', {'username': user.username, 'password': 'johnpassword'})
        self.assertEqual(response.url, '/core/')
        self.assertEqual(302, response.status_code)

    def test_get_turmas_(self):
        client = Client()
        url = '/core/turmas/his-lic'
        response = client.get(url)

        self.assertEqual(200, response.status_code)
