from django.shortcuts import render

from core.bo.turma import carrega_turmas, carrega_turmas_horario, atualiza_ano_periodo, atualiza_semestres


def turmas_grade(request, estrutura, turmas_list_link):

    semestres = request.GET.getlist('semestres')
    ano_periodo = request.GET.getlist('ano_periodo')

    turmas = carrega_turmas(estrutura, semestres, ano_periodo)

    turmas_por_horario = carrega_turmas_horario(turmas)

    periodo_selecionado = atualiza_ano_periodo(ano_periodo)
    semestres_selecionado = atualiza_semestres(semestres)

    context = {
        'estrutura': estrutura,
        'turmas_por_horario': turmas_por_horario,
        'periodo_selecionado': periodo_selecionado[0],
        'semestres_selecionado': semestres_selecionado,
        'turma_list_link': turmas_list_link,
    }

    return render(request, 'core/turmas/grade_horarios.html', context)
