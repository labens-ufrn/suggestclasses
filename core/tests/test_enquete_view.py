from unittest.case import TestCase

from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from core.models import Enquete, ComponenteCurricular
from core.tests.povoar_testes import criar_dados, remover_dados, criar_enquetes


class EnqueteViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super(EnqueteViewTests, cls).setUpClass()
        print('\nEnqueteViewTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def setUp(self):
        """Inicialização de cada Teste."""
        self.enquete:Enquete = criar_enquetes()

    def tearDown(self):
        """Finalização de cada Teste."""
        self.enquete.delete()

    def test_enquete_list(self):
        client = Client()
        response = client.get(reverse('search_enquetes'))

        self.assertEqual(200, response.status_code)


    def test_enquete_detail(self):
        client = Client()
        response = client.get(reverse('enquete_detalhar', args=(self.enquete.pk,)))

        self.assertEqual(200, response.status_code)


    def test_enquete_votos_listar(self):
        client = Client()

        user = User.objects.get(username='john')
        url = reverse('Login de Usuário')
        index = reverse('index')
        response = client.post(url, {'username': user.username, 'password': 'johnpassword'})
        self.assertEqual(response.url, index)


        cc = ComponenteCurricular.objects.get(id_componente=99999)
        url = reverse('enquete_votos_listar',
                      args=(self.enquete.pk,cc.pk))
        response = client.get(url)

        self.assertEqual(200, response.status_code)


