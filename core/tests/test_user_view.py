import django
django.setup()

from core.forms import CadastroUsuarioForm
from unittest.case import TestCase

from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase
from django.urls import reverse

from core.tests.povoar_testes import criar_dados, remover_dados


class UserViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nUserViewTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    def test_usuario_cadastrar(self):
        client = Client()
        url = reverse('Cadastro de Usuário')
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    def test_logar_usuario(self):
        client = Client()
        url = '/core/usuario/logar'
        response = client.get(url)

        self.assertEqual(200, response.status_code)

    # Valid Form Data
    def test_UserForm_valid(self):
        form = CadastroUsuarioForm(data={'email': "teste@thebeatles.com",
                                         'password1': "johnpassword",
                                         'password2': "johnpassword",
                                         'username': "test",
                                         'matricula': 9999998})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = CadastroUsuarioForm(data={'email': "lennon@thebeatles.com",
                                         'password1': "johnpassword",
                                         'password2': "johnpassword",
                                         'username': "john",
                                         'matricula': 9999998})
        self.assertFalse(form.is_valid())

    def test_home_view(self):
        client = Client()
        user_login = client.login(username="john", password="johnpassword")
        self.assertTrue(user_login)
        index = reverse('index')
        response = client.get(index)
        self.assertEqual(response.status_code, 200)

    def test_add_user_view_post(self):
        # Apagar o usuário caso ele já exista!
        if User.objects.filter(username='johnteste').exists():
            User.objects.get(username='johnteste').delete()
        user_count = User.objects.count()
        client = Client()
        # https://micropyramid.com/blog/django-unit-test-cases-with-forms-and-views/
        url = reverse('Cadastro de Usuário')
        # include url for add user view
        response = client.post(url, {'email': "teste@thebeatles.com",
                                     'password1': "johnpassword",
                                     'password2': "johnpassword",
                                     'username': "johnteste",
                                     'matricula': 9999996})
        # se passar no is_valid() o retorno é um redirecionamento.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), user_count + 1)
        # self.assertTrue('"error": false' in response.content)


class UserViewSimpleTests(SimpleTestCase):

    def test_add_user_view(self):
        client = Client()
        # https://micropyramid.com/blog/django-unit-test-cases-with-forms-and-views/
        url = reverse('Cadastro de Usuário')
        # include url for add user view
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'core/usuario/cadastro.html')
