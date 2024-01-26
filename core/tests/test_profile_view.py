import django
django.setup()

from core.forms import HistoricoForm
from unittest.case import TestCase

from django.contrib.auth.models import User
from django.test import Client, SimpleTestCase

from core.tests.povoar_testes import criar_dados, remover_dados


class ProfileViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nProfileViewTests')
        criar_dados()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        remover_dados()

    