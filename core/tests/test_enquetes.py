import django
django.setup()

from datetime import date, timedelta
from core.bo.enquetes import get_enquetes, get_enquetes_por_curso, get_componentes_enquete
from core.tests.povoar_testes import criar_dados, remover_dados
from core.models import Curso, Enquete

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

class EnqueteTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('\nEnqueteTests')
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

    def test_get_enquetes(self):
        enquete = get_enquetes()

        self.assertIsNotNone(enquete, 'Enquete não é None?')

    def test_get_enquetes_por_curso(self):
        enquete = get_enquetes_por_curso(7191770)
        self.assertIsNotNone(enquete, 'Enquete não é None?')
        # self.assertEqual()

    def test_get_componentes_enquete(self):
        enquete = get_enquetes_por_curso(7191770)
        print(enquete)
        pass

def criar_enquetes():
    curso = Curso.objects.get(codigo=9999)
    usuario1 = User.objects.get(username='docente1')
    enquete = Enquete.objects.create(
        nome = 'Enquete 0001',
        numero_votos = 6,
        data_hora_inicio = timezone.now() + timedelta(days=-10),
        data_hora_fim = timezone.now() + timedelta(days=10),
        curso = curso,
        status = Enquete.ATIVA,
        tipo = Enquete.COMPLETA,
        usuario = usuario1,
        criada_em = date.today() + timedelta(days=-11)
    )
    return enquete
