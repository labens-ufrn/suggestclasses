from django.contrib import messages
from django.shortcuts import render, redirect

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


def sugestao_manter(request, estrutura, sugestao_incluir_link, sugestao_grade_link):
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

