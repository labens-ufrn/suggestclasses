from core.models import PeriodoLetivo
from core.bo.periodos import get_periodo_ativo, get_periodo_letivo
from django.shortcuts import render

from core.bo.turma import atualiza_periodo_letivo, carrega_turmas, carrega_turmas_horario, atualiza_ano_periodo, atualiza_semestres


def turmas_grade(request, estrutura, turmas_list_link):

    semestres = request.GET.getlist('semestres')
    ano_periodo = request.GET.getlist('ano_periodo')
    periodo_selecionado = atualiza_periodo_letivo(ano_periodo)

    turmas = carrega_turmas(estrutura, semestres, periodo_selecionado)

    turmas_por_horario = carrega_turmas_horario(turmas)

    semestres_selecionado = atualiza_semestres(semestres)

    ano_periodo_atual = get_periodo_ativo()
    ano_periodo_anterior1 = None
    ano_periodo_anterior2 = None
    if ano_periodo_atual.periodo == 2:
        ano_anterior = ano_periodo_atual.ano
        periodo_anterior = 1
        ano_periodo_anterior1 = get_periodo_letivo(
            PeriodoLetivo.CONSOLIDADO,
            ano=ano_anterior,
            periodo=periodo_anterior).first()

        ano_anterior = ano_periodo_atual.ano-1
        periodo_anterior = 2
        ano_periodo_anterior2 = get_periodo_letivo(
            PeriodoLetivo.CONSOLIDADO,
            ano=ano_anterior, periodo=periodo_anterior).first()
    else:
        ano_anterior = ano_periodo_atual.ano-1
        periodo_anterior = 2
        ano_periodo_anterior1 = get_periodo_letivo(
            PeriodoLetivo.CONSOLIDADO,
            ano=ano_anterior,
            periodo=periodo_anterior).first()

        periodo_anterior = 1
        if (ano_anterior == 2020):
            periodo_anterior = 6

        ano_periodo_anterior2 = get_periodo_letivo(
            PeriodoLetivo.CONSOLIDADO,
            ano=ano_anterior, periodo=periodo_anterior).first()

    context = {
        'estrutura': estrutura,
        'turmas_por_horario': turmas_por_horario,
        'periodo_selecionado': periodo_selecionado,
        'semestres_selecionado': semestres_selecionado,
        'turma_list_link': turmas_list_link,
        'ano_periodo_atual': ano_periodo_atual,
        'ano_periodo_anterior1': ano_periodo_anterior1,
        'ano_periodo_anterior2': ano_periodo_anterior2,
    }

    return render(request, 'core/turmas/grade_horarios.html', context)
