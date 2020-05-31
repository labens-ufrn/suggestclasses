from django.contrib.auth.decorators import permission_required

from core.bo.sevices import get_estrutura_letras_espanhol, get_estrutura_letras_portugues, get_estrutura_letras_ingles
from core.visoes.suggest_view import sugestao_grade_horarios, sugestao_manter, sugestao_incluir, sugestao_editar, \
    sugestao_deletar


def sugestao_let_esp_list(request):
    let_esp_ec = get_estrutura_letras_espanhol()
    sugestao_incluir_link = '/core/sugestao/let-esp/incluir'
    sugestao_manter_link = '/core/sugestao/let-esp/manter'
    sugestao_list_link = '/core/sugestao/let-esp/list'
    return sugestao_grade_horarios(request, let_esp_ec, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_esp_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Letras - Língua Espanhola - Currais Novos.
    """
    let_esp_ec = get_estrutura_letras_espanhol()
    sugestao_incluir_link = '/core/sugestao/let-esp/incluir'
    sugestao_editar_link = 'sugestao_let_esp_editar'
    sugestao_deletar_link = 'sugestao_let_esp_deletar'
    sugestao_grade_link = '/core/sugestao/let-esp/list'
    return sugestao_manter(request, let_esp_ec, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_esp_incluir(request):
    let_esp_ec = get_estrutura_letras_espanhol()
    sugestao_manter_link = '/core/sugestao/let-esp/manter'
    return sugestao_incluir(request, let_esp_ec, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_esp_editar(request, pk):
    let_esp_ec = get_estrutura_letras_espanhol()
    return sugestao_editar(request, pk, estrutura=let_esp_ec)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_esp_deletar(request, pk):
    let_esp_ec = get_estrutura_letras_espanhol()
    return sugestao_deletar(request, pk, estrutura=let_esp_ec)


def sugestao_let_por_list(request):
    let_por_ec = get_estrutura_letras_portugues()
    sugestao_incluir_link = '/core/sugestao/let-por/incluir'
    sugestao_manter_link = '/core/sugestao/let-por/manter'
    sugestao_list_link = '/core/sugestao/let-por/list'
    return sugestao_grade_horarios(request, let_por_ec, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_por_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Letras - Língua Portuguesa - Currais Novos.
    """
    let_por_ec = get_estrutura_letras_portugues()
    sugestao_incluir_link = '/core/sugestao/let-por/incluir'
    sugestao_editar_link = 'sugestao_let_por_editar'
    sugestao_deletar_link = 'sugestao_let_por_deletar'
    sugestao_grade_link = '/core/sugestao/let-por/list'
    return sugestao_manter(request, let_por_ec, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_por_incluir(request):
    let_por_ec = get_estrutura_letras_portugues()
    sugestao_manter_link = '/core/sugestao/let-por/manter'
    return sugestao_incluir(request, let_por_ec, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_por_editar(request, pk):
    let_por_ec = get_estrutura_letras_portugues()
    return sugestao_editar(request, pk, estrutura=let_por_ec)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_por_deletar(request, pk):
    let_por_ec = get_estrutura_letras_portugues()
    return sugestao_deletar(request, pk, estrutura=let_por_ec)


def sugestao_let_ing_list(request):
    let_ing_ec = get_estrutura_letras_ingles()
    sugestao_incluir_link = '/core/sugestao/let-ing/incluir'
    sugestao_manter_link = '/core/sugestao/let-ing/manter'
    sugestao_list_link = '/core/sugestao/let-ing/list'
    return sugestao_grade_horarios(request, let_ing_ec, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_ing_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Letras - Língua Inglesa - Currais Novos.
    """
    let_ing_ec = get_estrutura_letras_ingles()
    sugestao_incluir_link = '/core/sugestao/let-ing/incluir'
    sugestao_editar_link = 'sugestao_let_ing_editar'
    sugestao_deletar_link = 'sugestao_let_ing_deletar'
    sugestao_grade_link = '/core/sugestao/let-ing/list'
    return sugestao_manter(request, let_ing_ec, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_ing_incluir(request):
    let_ing_ec = get_estrutura_letras_ingles()
    sugestao_manter_link = '/core/sugestao/let-ing/manter'
    return sugestao_incluir(request, let_ing_ec, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_ing_editar(request, pk):
    let_ing_ec = get_estrutura_letras_ingles()
    return sugestao_editar(request, pk, estrutura=let_ing_ec)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_let_ing_deletar(request, pk):
    let_ing_ec = get_estrutura_letras_ingles()
    return sugestao_deletar(request, pk, estrutura=let_ing_ec)
