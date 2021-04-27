from django.contrib.auth.decorators import permission_required

from core.bo.sevices import get_estrutura_historia_bacharelado, get_estrutura_historia_licenciatura
from core.visoes.suggest_view import (sugestao_deletar, sugestao_editar, sugestao_grade_horarios, sugestao_incluir, sugestao_manter)


def sugestao_his_bac_list(request):
    his_bac_ec = get_estrutura_historia_bacharelado()
    sugestao_incluir_link = '/core/sugestao/his-bac/incluir'
    sugestao_manter_link = '/core/sugestao/his-bac/manter'
    sugestao_list_link = '/core/sugestao/his-bac'
    return sugestao_grade_horarios(request, his_bac_ec, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_his_bac_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de História - Bacharelado - Caicó.
    """
    his_bac_ec = get_estrutura_historia_bacharelado()
    sugestao_incluir_link = '/core/sugestao/his-bac/incluir'
    sugestao_editar_link = 'sugestao_his_bac_editar'
    sugestao_deletar_link = 'sugestao_his_bac_deletar'
    sugestao_grade_link = '/core/sugestao/his-bac'
    return sugestao_manter(request, his_bac_ec, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_his_bac_incluir(request):
    his_bac_ec = get_estrutura_historia_bacharelado()
    sugestao_manter_link = '/core/sugestao/his-bac/manter'
    return sugestao_incluir(request, his_bac_ec, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_his_bac_editar(request, pk):
    his_bac_ec = get_estrutura_historia_bacharelado()
    return sugestao_editar(request, pk, estrutura=his_bac_ec)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_his_bac_deletar(request, pk):
    his_bac_ec = get_estrutura_historia_bacharelado()
    return sugestao_deletar(request, pk, estrutura=his_bac_ec)


def sugestao_his_lic_list(request):
    his_lic_ec = get_estrutura_historia_licenciatura()
    sugestao_incluir_link = '/core/sugestao/his-lic/incluir'
    sugestao_manter_link = '/core/sugestao/his-lic/manter'
    sugestao_list_link = '/core/sugestao/his-lic'
    return sugestao_grade_horarios(request, his_lic_ec, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_his_lic_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de História - Licenciatura - Caicó.
    """
    his_lic_ec = get_estrutura_historia_licenciatura()
    sugestao_incluir_link = '/core/sugestao/his-lic/incluir'
    sugestao_editar_link = 'sugestao_his_lic_editar'
    sugestao_deletar_link = 'sugestao_his_lic_deletar'
    sugestao_grade_link = '/core/sugestao/his-lic'
    return sugestao_manter(request, his_lic_ec, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_his_lic_incluir(request):
    his_lic_ec = get_estrutura_historia_licenciatura()
    sugestao_manter_link = '/core/sugestao/his-lic/manter'
    return sugestao_incluir(request, his_lic_ec, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_his_lic_editar(request, pk):
    his_lic_ec = get_estrutura_historia_licenciatura()
    return sugestao_editar(request, pk, estrutura=his_lic_ec)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_his_lic_deletar(request, pk):
    his_lic_ec = get_estrutura_historia_licenciatura()
    return sugestao_deletar(request, pk, estrutura=his_lic_ec)
