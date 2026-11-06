import django
django.setup()

from django.contrib.auth.models import Permission, User
from django.test import Client, TestCase
from django.urls import reverse

from core.models import EstruturaCurricular
from core.tests.povoar_testes import criar_dados

# Identificadores fixos usados por core/bo/sevices.py para Geografia (Caicó).
ID_EC_GEO_BAC = 89306921
ID_EC_GEO_LIC = 89189948


def _clonar_estrutura(id_curriculo_origem, novo_id_curriculo):
    """Cria uma estrutura curricular com o id_curriculo esperado pelas views,
    a partir de uma estrutura do povoamento de testes."""
    estrutura = EstruturaCurricular.objects.get(id_curriculo=id_curriculo_origem)
    estrutura.pk = None
    estrutura.id_curriculo = novo_id_curriculo
    estrutura.save()
    return estrutura


class SugestaoGeografiaViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('\nSugestaoGeografiaViewTests')
        criar_dados()
        _clonar_estrutura(999999999, ID_EC_GEO_BAC)
        _clonar_estrutura(999999998, ID_EC_GEO_LIC)

        cls.usuario_sem_permissao = User.objects.create_user('geo_sem_perm', password='senha-teste')
        cls.usuario_com_permissao = User.objects.create_user('geo_com_perm', password='senha-teste')
        cls.usuario_com_permissao.user_permissions.add(
            Permission.objects.get(content_type__app_label='core', codename='change_sugestaoturma'))

    def assert_redireciona_para_raiz(self, response):
        """O handler403 do projeto (core/views.py:error_403) converte a negação
        de permissão em redirect 302 para '/', e não em resposta 403."""
        self.assertEqual(302, response.status_code)
        self.assertEqual('/', response.url)

    def test_geo_bac_list_publica(self):
        response = Client().get(reverse('sugestao_geo_bac_list'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(ID_EC_GEO_BAC, response.context['estrutura'].id_curriculo)

    def test_geo_lic_list_publica(self):
        response = Client().get(reverse('sugestao_geo_lic_list'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(ID_EC_GEO_LIC, response.context['estrutura'].id_curriculo)

    def test_geo_bac_manter_anonimo_rejeitado(self):
        response = Client().get(reverse('sugestao_geo_bac_manter'))

        self.assert_redireciona_para_raiz(response)

    def test_geo_lic_manter_anonimo_rejeitado(self):
        response = Client().get(reverse('sugestao_geo_lic_manter'))

        self.assert_redireciona_para_raiz(response)

    def test_geo_bac_manter_sem_permissao_rejeitado(self):
        client = Client()
        client.force_login(self.usuario_sem_permissao)

        response = client.get(reverse('sugestao_geo_bac_manter'))

        self.assert_redireciona_para_raiz(response)

    def test_geo_bac_manter_com_permissao(self):
        client = Client()
        client.force_login(self.usuario_com_permissao)

        response = client.get(reverse('sugestao_geo_bac_manter'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(ID_EC_GEO_BAC, response.context['estrutura'].id_curriculo)
        self.assertEqual('sugestao_geo_bac_editar', response.context['sugestao_editar_link'])

    def test_geo_lic_manter_com_permissao(self):
        client = Client()
        client.force_login(self.usuario_com_permissao)

        response = client.get(reverse('sugestao_geo_lic_manter'))

        self.assertEqual(200, response.status_code)
        self.assertEqual(ID_EC_GEO_LIC, response.context['estrutura'].id_curriculo)
        self.assertEqual('sugestao_geo_lic_editar', response.context['sugestao_editar_link'])

    def test_geo_bac_incluir_anonimo_rejeitado(self):
        response = Client().post(reverse('sugestao_geo_bac_incluir'))

        self.assert_redireciona_para_raiz(response)
