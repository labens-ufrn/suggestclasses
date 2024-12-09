import django
django.setup()

from core.bo.enquetes import get_enquetes, get_enquetes_por_curso, get_componentes_enquete
from core.tests.povoar_testes import criar_dados, remover_dados, criar_enquetes
from core.models import Enquete

from django.test import TestCase

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


