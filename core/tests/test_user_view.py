import os
import django
import pytest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from core.forms import CadastroUsuarioForm
from unittest.case import TestCase

from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase
from django.urls import reverse

from core.models import SugestaoTurma
from core.tests.povoar_testes import criar_dados, remover_dados


@pytest.mark.django_db
class UserViewTests(TestCase):

    def setUp(self):
        criar_dados()

    def tearDown(self):
        remover_dados()

    def test_usuario_cadastrar(self):
        client = Client()
        url = '/core/usuario/cadastrar'
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
        response = client.get("/core/")
        self.assertEqual(response.status_code, 200)

    def test_add_user_view_post(self):
        client = Client()
        # https://micropyramid.com/blog/django-unit-test-cases-with-forms-and-views/
        url = '/core/usuario/cadastrar'
        # include url for add user view
        response = client.post(url, {'email': "teste@thebeatles.com",
                                     'password1': "johnpassword",
                                     'password2': "johnpassword",
                                     'username': "johnteste",
                                     'matricula': 9999996})
        self.assertEqual(response.status_code, 200)


class UserViewSimpleTests(SimpleTestCase):

    def test_add_user_view(self):
        client = Client()
        # https://micropyramid.com/blog/django-unit-test-cases-with-forms-and-views/
        url = '/core/usuario/cadastrar'
        # include url for add user view
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'core/usuario/cadastro.html')
