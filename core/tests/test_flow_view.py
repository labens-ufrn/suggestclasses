import django
django.setup()

from django.test import Client, TestCase
from django.urls import reverse

from core.tests.povoar_testes import criar_dados

# (nome da rota, status esperado)
ROTAS_FLUXOGRAMA = [
    ('Lista de Fluxogramas', 200),
    ('Fluxograma BSI - 01B - Horizontal', 200),
    ('Fluxograma BSI - Opcionais', 200),
    ('flow_cont', 200),
    ('flow_cont_op', 200),
    ('flow_dir', 200),
    ('flow_dir_op', 200),
    ('flow_his_lic', 200),
    ('flow_his_lic_op', 200),
    ('flow_his_bac', 200),
    ('flow_his_bac_op', 200),
    ('flow_geo_lic', 200),
    ('flow_geo_lic_op', 200),
    ('flow_geo_bac', 200),
    ('flow_geo_bac_op', 200),
    ('flow_ped_h', 200),
    ('Fluxograma Pedagogia - Opcionais', 200),
    ('flow_let_esp', 200),
    ('flow_let_esp_op', 200),
    ('flow_let_por', 200),
    ('flow_let_por_op', 200),
    ('flow_let_ing', 200),
    ('flow_let_ing_op', 200),
    ('flow_mat_h', 200),
    ('flow_mat_op', 200),
    ('flow_adm', 200),
    ('flow_adm_op', 200),
    ('flow_tur', 200),
    ('flow_tur_op', 200),
]


class FlowViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('\nFlowViewTests')
        criar_dados()

    def test_rotas_de_fluxograma(self):
        client = Client()

        for nome, status in ROTAS_FLUXOGRAMA:
            with self.subTest(rota=nome):
                response = client.get(reverse(nome))

                self.assertEqual(status, response.status_code)
                if status == 200:
                    self.assertTrue(response.templates, 'a view não renderizou template')
