import django
django.setup()

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from core.tests.povoar_testes import criar_dados


class ProfileViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('\nProfileViewTests')
        criar_dados()
        cls.john = User.objects.get(username='john')

    def test_profile_proprio_usuario(self):
        client = Client()
        client.force_login(self.john)

        response = client.get(reverse('profile', args=(self.john.username,)))

        self.assertEqual(200, response.status_code)
        self.assertEqual(self.john, response.context['usuario'])
        self.assertTemplateUsed(response, 'core/usuario/profile.html')

    def test_profile_de_outro_usuario_redireciona(self):
        client = Client()
        client.force_login(self.john)

        response = client.get(reverse('profile', args=('docente1',)))

        self.assertEqual(302, response.status_code)

    def test_profile_anonimo_redireciona_para_login(self):
        response = Client().get(reverse('profile', args=(self.john.username,)))

        self.assertEqual(302, response.status_code)
        self.assertIn('login', response.url)
