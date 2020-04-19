from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from core.bo.docente import get_funcao_by_siape
from core.bo.turma import atualiza_semestres, carrega_sugestao_turmas, carrega_turmas_horario
from core.config.config import get_config
from core.forms import SugestaoTurmaForm


def sugestao_grade_horarios(request, estrutura, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link):
    semestres = request.GET.getlist('semestres')
    semestres = atualiza_semestres(semestres)

    config = get_config()
    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')

    turmas = carrega_sugestao_turmas(estrutura, semestres, ano, periodo)

    tt = carrega_turmas_horario(turmas)

    context = {
        'tt': tt,
        'estrutura': estrutura,
        'ano_periodo': ano_periodo,
        'semestres_atual': semestres,
        'sugestao_incluir_link': sugestao_incluir_link,
        'sugestao_manter_link': sugestao_manter_link,
        'sugestao_list_link': sugestao_list_link,
    }

    return render(request, 'core/sugestao/grade_horarios.html', context)


def sugestao_manter(request, estrutura, sugestao_incluir_link, sugestao_grade_link, sugestao_editar_link):
    """
            Lista todas as salas do centro.
    """
    # Todos os Semestres
    semestres = ['100']
    semestres = atualiza_semestres(semestres)

    config = get_config()
    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')

    st_list = carrega_sugestao_turmas(estrutura, semestres, ano, periodo)

    context = {
        'ano_periodo': ano_periodo,
        'estrutura': estrutura,
        'sugestao_incluir_link': sugestao_incluir_link,
        'sugestao_editar_link': sugestao_editar_link,
        'sugestao_grade_link': sugestao_grade_link,
        'sugestao_list': st_list
    }

    return render(request, 'core/sugestao/manter.html', context)


def sugestao_incluir(request, estrutura, sugestao_manter_link):
    config = get_config()
    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')

    if request.method == "POST":
        form_sugestao = SugestaoTurmaForm(request.POST, estrutura=estrutura)
        if form_sugestao.is_valid():
            sugestao_turma = form_sugestao.save(commit=False)
            sugestao_turma.tipo = 'REGULAR'
            sugestao_turma.ano = ano
            sugestao_turma.periodo = periodo
            sugestao_turma.campus_turma = sugestao_turma.local.campus
            sugestao_turma.criador = request.user
            sugestao_turma.total_solicitacoes = 0
            sugestao_turma.save()
            messages.success(request, 'Sugestão de Turma cadastrada com sucesso.')
            return redirect(sugestao_manter_link)
        else:
            messages.error(request, form_sugestao.errors['__all__'])
    else:
        form_sugestao = SugestaoTurmaForm(estrutura=estrutura)
        context = {
            'ano_periodo': ano_periodo,
            'estrutura': estrutura,
            'form_sugestao': form_sugestao,
        }
    return render(request, 'core/sugestao/incluir.html', context)


def verificar_permissoes(request, sugestao):
    # Verificar se o Usuário é o criador da Sugestão de Turma
    usuario = request.user
    departamento = sugestao.componente.departamento
    if is_criador(usuario, sugestao):
        return True
    # Verificar se o Usuário é o chefe do Departamento da Sugestão de Turma
    if is_chefe(usuario, departamento):
        return True
    return False


def is_criador(usuario, sugestao):
    """
    Verificar se o Usuário é o criador da Sugestão de Turma.
    :param usuario: Usuário autenticado.
    :param sugestao: Sugestão de Turma.
    :return: True se o usuário for o criador da Sugestão de Turma.
    """
    return usuario == sugestao.criador


def is_chefe(usuario, departamento):
    """
    Verificar se o Usuário tem a Função de Chefe de Departamento.
    :param usuario: Usuário autenticado.
    :param departamento: O departamento de interesse.
    :return: True se o usuário for Chefe do Departamento.
    """
    grupo_chefes = Group.objects.get(name='Chefes')
    grupos = usuario.groups.all()

    id_unidade_lotacao = usuario.docente.id_unidade_lotacao
    test_chefe1 = departamento.id_unidade == id_unidade_lotacao

    siape = usuario.docente.siape
    funcao = get_funcao_by_siape(siape)
    id_unidade_designacao = funcao[0].id_unidade_designacao
    test_chefe2 = departamento.id_unidade == id_unidade_designacao

    return grupo_chefes in grupos and test_chefe1 and test_chefe2
