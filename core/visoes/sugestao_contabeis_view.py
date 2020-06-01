from django.contrib.auth.decorators import permission_required

from core.bo.sevices import get_estrutura_contabeis
from core.visoes.suggest_view import sugestao_grade_horarios, sugestao_manter, sugestao_incluir, sugestao_editar, \
    sugestao_deletar


def sugestao_cont_list(request):
    """
    Tela de Listar as Sugestões de Turmas do Curso de Ciências Contábeis - Caicó.
    """
    contabeis_ec = get_estrutura_contabeis()
    sugestao_incluir_link = '/core/sugestao/cont/incluir'
    sugestao_manter_link = '/core/sugestao/cont/manter'
    sugestao_list_link = '/core/sugestao/cont/list'
    return sugestao_grade_horarios(
        request, contabeis_ec, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_cont_manter(request):
    """
    Tela de Manter Sugestões de Turmas do Curso de Ciências Contábeis - Caicó.
    """
    contabeis_ec = get_estrutura_contabeis()
    sugestao_incluir_link = '/core/sugestao/cont/incluir'
    sugestao_editar_link = 'sugestao_cont_editar'
    sugestao_deletar_link = 'sugestao_cont_deletar'
    sugestao_grade_link = '/core/sugestao/cont/list'
    return sugestao_manter(request, contabeis_ec, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_cont_incluir(request):
    """
    Tela de Incluir Sugestão de Turmas do Curso de Ciências Contábeis - Caicó.
    """
    contabeis_ec = get_estrutura_contabeis()
    sugestao_manter_link = '/core/sugestao/adm/manter'
    return sugestao_incluir(request, contabeis_ec, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_cont_editar(request, pk):
    """
    Tela de Editar Sugestão de Turmas do Curso de Ciências Contábeis - Caicó.
    """
    contabeis_ec = get_estrutura_contabeis()
    return sugestao_editar(request, pk, estrutura=contabeis_ec)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_cont_deletar(request, pk):
    """
    Tela de Deletar Sugestão de Turmas do Curso de Ciências Contábeis - Caicó.
    """
    contabeis_ec = get_estrutura_contabeis()
    return sugestao_deletar(request, pk, estrutura=contabeis_ec)
