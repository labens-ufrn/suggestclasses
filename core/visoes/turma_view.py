from core.models import PeriodoLetivo
from core.bo.periodos import get_periodo_ativo, get_periodo_letivo
from django.shortcuts import render

from core.bo.turma import atualiza_periodo_letivo, carrega_turmas, carrega_turmas_horario, atualiza_ano_periodo, atualiza_semestres


def turmas_grade(request, estrutura, turmas_list_link):

    semestres = request.GET.getlist('semestres')
    ano_periodo = request.GET.getlist('ano_periodo')

    turmas = carrega_turmas(estrutura, semestres, ano_periodo)

    turmas_por_horario = carrega_turmas_horario(turmas)

    atualiza_periodo_letivo(ano_periodo)
    periodo_selecionado = atualiza_ano_periodo(ano_periodo)
    semestres_selecionado = atualiza_semestres(semestres)

    ano_periodo_atual = get_periodo_ativo()
    ano_periodo_anterior1 = None
    ano_periodo_anterior2 = None
    if ano_periodo_atual.periodo == 2:
        ano_periodo_anterior1 = get_periodo_letivo(
            PeriodoLetivo.CONSOLIDADO,
            ano=ano_periodo_atual.ano,
            periodo=1).first()
        ano_periodo_anterior2 = get_periodo_letivo(
            PeriodoLetivo.CONSOLIDADO,
            ano=ano_periodo_atual.ano-1, periodo=2).first()
    else:
        ano_periodo_anterior1 = get_periodo_letivo(
            PeriodoLetivo.CONSOLIDADO,
            ano=ano_periodo_atual.ano-1,
            periodo=2).first()
        ano_periodo_anterior2 = get_periodo_letivo(
            PeriodoLetivo.CONSOLIDADO,
            ano=ano_periodo_atual.ano-1, periodo=1).first()

    context = {
        'estrutura': estrutura,
        'turmas_por_horario': turmas_por_horario,
        'periodo_selecionado': periodo_selecionado[0],
        'semestres_selecionado': semestres_selecionado,
        'turma_list_link': turmas_list_link,
        'ano_periodo_atual': ano_periodo_atual,
        'ano_periodo_anterior1': ano_periodo_anterior1,
        'ano_periodo_anterior2': ano_periodo_anterior2,
    }

    return render(request, 'core/turmas/grade_horarios.html', context)
