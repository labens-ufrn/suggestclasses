from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods
from core.bo.sevices import get_estrutura_geografia_bacharelado, get_estrutura_geografia_licenciatura
from core.visoes.suggest_view import (sugestao_deletar, sugestao_editar, sugestao_grade_horarios, sugestao_incluir, sugestao_manter)

@require_http_methods(["GET"])
def sugestao_geo_bac_list(request):
    geo_bac_ec = get_estrutura_geografia_bacharelado()
    sugestao_incluir_link = '/core/sugestao/geo-bac/incluir'
    sugestao_manter_link = '/core/sugestao/geo-bac/manter'
    sugestao_list_link = '/core/sugestao/geo-bac'
    return sugestao_grade_horarios(request, geo_bac_ec, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
@require_http_methods(["GET"])
def sugestao_geo_bac_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Geografia - Bacharelado - Caicó.
    """
    geo_bac_ec = get_estrutura_geografia_bacharelado()
    sugestao_incluir_link = '/core/sugestao/geo-bac/incluir'
    sugestao_editar_link = 'sugestao_geo_bac_editar'
    sugestao_deletar_link = 'sugestao_geo_bac_deletar'
    sugestao_grade_link = '/core/sugestao/geo-bac'
    return sugestao_manter(request, geo_bac_ec, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
@require_http_methods(["POST"])
def sugestao_geo_bac_incluir(request):
    geo_bac_ec = get_estrutura_geografia_bacharelado()
    sugestao_manter_link = '/core/sugestao/geo-bac/manter'
    return sugestao_incluir(request, geo_bac_ec, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
@require_http_methods(["POST"])
def sugestao_geo_bac_editar(request, pk):
    geo_bac_ec = get_estrutura_geografia_bacharelado()
    return sugestao_editar(request, pk, estrutura=geo_bac_ec)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
@require_http_methods(["POST"])
def sugestao_geo_bac_deletar(request, pk):
    geo_bac_ec = get_estrutura_geografia_bacharelado()
    return sugestao_deletar(request, pk, estrutura=geo_bac_ec)

@require_http_methods(["GET"])
def sugestao_geo_lic_list(request):
    geo_lic_ec = get_estrutura_geografia_licenciatura()
    sugestao_incluir_link = '/core/sugestao/geo-lic/incluir'
    sugestao_manter_link = '/core/sugestao/geo-lic/manter'
    sugestao_list_link = '/core/sugestao/geo-lic'
    return sugestao_grade_horarios(request, geo_lic_ec, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
@require_http_methods(["GET"])
def sugestao_geo_lic_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Geografia - Licenciatura - Caicó.
    """
    geo_lic_ec = get_estrutura_geografia_licenciatura()
    sugestao_incluir_link = '/core/sugestao/geo-lic/incluir'
    sugestao_editar_link = 'sugestao_geo_lic_editar'
    sugestao_deletar_link = 'sugestao_geo_lic_deletar'
    sugestao_grade_link = '/core/sugestao/geo-lic'
    return sugestao_manter(request, geo_lic_ec, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
@require_http_methods(["POST"])
def sugestao_geo_lic_incluir(request):
    geo_lic_ec = get_estrutura_geografia_licenciatura()
    sugestao_manter_link = '/core/sugestao/geo-lic/manter'
    return sugestao_incluir(request, geo_lic_ec, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
@require_http_methods(["POST"])
def sugestao_geo_lic_editar(request, pk):
    geo_lic_ec = get_estrutura_geografia_licenciatura()
    return sugestao_editar(request, pk, estrutura=geo_lic_ec)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
@require_http_methods(["POST"])
def sugestao_geo_lic_deletar(request, pk):
    geo_lic_ec = get_estrutura_geografia_licenciatura()
    return sugestao_deletar(request, pk, estrutura=geo_lic_ec)
