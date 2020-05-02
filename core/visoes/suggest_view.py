import logging
from typing import Set
from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from core.bo.docente import get_funcao_by_siape
from core.bo.sevices import get_organizacao_by_componente
from core.bo.sugestao import solicitacao_incluir
from core.bo.turma import atualiza_semestres, carrega_sugestao_turmas, carrega_turmas_horario, converte_desc_horario, \
    TurmaHorario
from core.config.config import get_config
from core.forms import SugestaoTurmaForm
from core.models import SugestaoTurma, SolicitacaoTurma, Horario
from mysite.settings import DOMAINS_WHITELIST

logger = logging.getLogger('suggestclasses.logger')
config = get_config()


def sugestao_grade_horarios(request, estrutura, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link):
    semestres = request.GET.getlist('semestres')
    semestres = atualiza_semestres(semestres)

    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')

    turmas = carrega_sugestao_turmas(estrutura, semestres, ano, periodo)

    tt = carrega_turmas_horario(turmas)

    context = {
        'tt': tt,
        'estrutura': estrutura,
        'ano_periodo': ano_periodo,
        'semestres_atual': criar_string(semestres) + '.',
        'sugestao_incluir_link': sugestao_incluir_link,
        'sugestao_manter_link': sugestao_manter_link,
        'sugestao_list_link': sugestao_list_link,
    }

    return render(request, 'core/sugestao/grade_horarios.html', context)


def sugestao_manter(request, estrutura, sugestao_incluir_link, sugestao_grade_link,
                    sugestao_editar_link, sugestao_deletar_link):
    """
            Lista todas as salas do centro.
    """
    # Todos os Semestres
    semestres = ['100']
    semestres = atualiza_semestres(semestres)

    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')

    st_list = carrega_sugestao_turmas(estrutura, semestres, ano, periodo)
    st_list = sorted(st_list, key=lambda sc: sc.componente.nome)

    context = {
        'ano_periodo': ano_periodo,
        'estrutura': estrutura,
        'sugestao_incluir_link': sugestao_incluir_link,
        'sugestao_editar_link': sugestao_editar_link,
        'sugestao_deletar_link': sugestao_deletar_link,
        'sugestao_grade_link': sugestao_grade_link,
        'sugestao_list': st_list
    }

    return render(request, 'core/sugestao/manter.html', context)


def sugestao_incluir(request, estrutura, sugestao_manter_link):
    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')

    if request.method == "POST":
        form_sugestao = SugestaoTurmaForm(request.POST, estrutura=estrutura)
        if form_sugestao.is_valid():
            sugestao_turma = form_sugestao.save(commit=False)
            carregar_dados(request, sugestao_turma, estrutura)
            horarios_list = converte_desc_horario(sugestao_turma.descricao_horario)
            if not verificar_existencia(form_sugestao, sugestao_turma) \
               and not verificar_choques(form_sugestao, sugestao_turma, horarios_list):
                sugestao_turma.save()
                atualizar_horarios(sugestao_turma, horarios_list)
                messages.success(request, 'Sugestão de Turma cadastrada com sucesso.')
                return redirect(sugestao_manter_link)
        messages.error(request, form_sugestao.errors)
    else:
        form_sugestao = SugestaoTurmaForm(estrutura=estrutura)

    context = {
        'ano_periodo': ano_periodo,
        'estrutura': estrutura,
        'form_sugestao': form_sugestao,
    }
    return render(request, 'core/sugestao/incluir.html', context)


def atualizar_horarios(sugestao, novos_horarios):
    # limpa o conjunto de horários
    sugestao.horarios.clear()
    # adiciona os novos horários
    sugestao.horarios.set(novos_horarios)


def carregar_dados(request, sugestao_turma, estrutura):
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')

    sugestao_turma.tipo = 'REGULAR'
    sugestao_turma.ano = ano
    sugestao_turma.periodo = periodo
    sugestao_turma.campus_turma = sugestao_turma.local.campus
    sugestao_turma.criador = request.user
    sugestao_turma.total_solicitacoes = 0

    org_curricular = get_organizacao_by_componente(estrutura, sugestao_turma.componente)
    sugestao_turma.semestre = org_curricular.first().semestre
    sugestao_turma.tipo_vinculo = org_curricular.first().tipo_vinculo
    sugestao_turma.curso = estrutura.curso


def verificar_existencia(form_sugestao, sugestao_turma):
    sugestoes = SugestaoTurma.objects.filter(
        codigo_turma=sugestao_turma.codigo_turma,
        componente=sugestao_turma.componente,
        ano=sugestao_turma.ano,
        periodo=sugestao_turma.periodo).values('codigo_turma')
    if sugestoes.exists():
        sugestoes = SugestaoTurma.objects.filter(
            componente=sugestao_turma.componente,
            ano=sugestao_turma.ano,
            periodo=sugestao_turma.periodo).values_list('codigo_turma')
        codigos_str = criar_string(sugestoes)
        form_sugestao.add_error('codigo_turma',
                                'Os seguintes códigos de turmas já foram utilizados: ' + codigos_str + '.')
        return True
    return False


def verificar_choques(form_sugestao, sugestao_turma, horarios_list):
    choques_componentes = set()
    choques_horarios = []
    choque_docente = []
    for horario in horarios_list:
        sugestoes = horario.sugestoes.all()
        if sugestoes:
            for s in sugestoes:
                if s.codigo_turma == sugestao_turma.codigo_turma and s.componente == sugestao_turma.componente:
                    break
                if s.local == sugestao_turma.local:
                    choques_componentes.add(str(s.componente.codigo) + ' - ' + s.componente.nome)
                    choques_horarios.append(horario.dia + horario.turno + horario.ordem)
                if s.docente == sugestao_turma.docente:
                    choques_componentes.add(str(s.componente.codigo) + ' - ' + s.componente.nome)
                    choque_docente.append(horario.dia + horario.turno + horario.ordem)

    if choques_horarios or choque_docente or choques_componentes:
        if choques_componentes:
            form_sugestao.add_error('componente',
                                    'Choque com os Componentes Curriculares: ' +
                                    criar_string(list(choques_componentes)) + '.')
        if choques_horarios:
            form_sugestao.add_error('local',
                                    'Sala com choque nos horários: ' +
                                    criar_string(choques_horarios) + '.')
        if choque_docente:
            form_sugestao.add_error('docente',
                                    'Docente com choque nos horários: ' +
                                    criar_string(choque_docente) + '.')
        return True
    return False


def criar_string(colecao):
    str_result = ''
    tam = len(colecao)
    for index, s in enumerate(colecao, start=1):
        str_result += s.__str__()
        if tam > 1 and index < tam:
            str_result += ', '
    str_result += ''
    return str_result


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_editar(request, pk, estrutura, template_name='core/sugestao/editar.html'):
    sugestao = get_object_or_404(SugestaoTurma, pk=pk)
    if not verificar_permissoes(request, sugestao, estrutura):
        messages.error(request, 'Você não tem permissão de Editar esta Sugestão de Turma.')
        return redirecionar(request)
    form_sugestao = SugestaoTurmaForm(request.POST or None, instance=sugestao, estrutura=estrutura)
    if form_sugestao.is_valid():
        sugestao_turma = form_sugestao.save(commit=False)
        horarios_list = converte_desc_horario(sugestao_turma.descricao_horario)
        if not verificar_choques(form_sugestao, sugestao_turma, horarios_list):
            sugestao_turma.save()
            sugestao_turma.horarios.clear()  # limpa o conjunto de horários
            sugestao_turma.horarios.set(horarios_list)  # adiciona os novos horários

            messages.success(request, 'Sugestão de Turma alterada com sucesso.')
            return redirecionar(request)
    else:
        messages.error(request, form_sugestao.errors)
    return render(request, template_name, {'form': form_sugestao})


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_deletar(request, pk, estrutura, template_name='core/sugestao/confirm_delete.html'):
    sugestao = get_object_or_404(SugestaoTurma, pk=pk)
    if not verificar_permissoes(request, sugestao, estrutura):
        messages.error(request, 'Você não tem permissão de Excluir esta Sugestão de Turma.')
        return redirecionar(request)
    if request.method == 'POST':
        sugestao.delete()
        messages.success(request, 'Sugestão de Turma excluída com sucesso.')
        return redirecionar(request)
    return render(request, template_name, {'object': sugestao})


def redirecionar(request):
    url = request.GET.get("next", "/")
    parsed_uri = urlparse(url)
    if parsed_uri.netloc == '' or parsed_uri.netloc in DOMAINS_WHITELIST:
        return HttpResponseRedirect(url)
    return HttpResponseRedirect("/core")


def verificar_permissoes(request, sugestao, estrutura):
    # Verificar se o Usuário é o criador da Sugestão de Turma
    usuario = request.user
    departamento = sugestao.componente.departamento
    if is_criador(usuario, sugestao):
        return True
    # Verificar se o Usuário é o Chefe do Departamento da Sugestão de Turma
    if is_chefe(usuario, departamento):
        return True
    # Verificar se o Usuário é o Coordenador do Curso da Sugestão de Turma
    if is_coordenador(usuario, estrutura.curso):
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
    if not docente_existe(usuario):
        return False

    grupo_chefes = Group.objects.get(name='Chefes')
    grupos = usuario.groups.all()

    id_unidade_lotacao = usuario.docente.id_unidade_lotacao
    test_chefe1 = departamento.id_unidade == id_unidade_lotacao

    siape = usuario.docente.siape
    funcao = get_funcao_by_siape(siape)
    id_unidade_designacao = funcao[0].id_unidade_designacao
    test_chefe2 = departamento.id_unidade == id_unidade_designacao

    return grupo_chefes in grupos and test_chefe1 and test_chefe2


def is_coordenador(usuario, curso):
    """
    Verificar se o Usuário tem a Função de Coordenador de Curso.
    :param usuario: Usuário autenticado.
    :param curso: O curso de interesse.
    :return: True se o usuário for Coordenador do Curso.
    """
    if not docente_existe(usuario):
        return False

    grupo_chefes = Group.objects.get(name='Coordenadores')
    grupos = usuario.groups.all()

    siape = usuario.docente.siape
    test_coordenador1 = curso.coordenador.siape == siape

    funcoes = get_funcao_by_siape(siape)
    test_coordenador2 = False
    for funcao in funcoes:
        # id_unidade_designacao = funcao.id_unidade_designacao
        # O id_unidade de curso não existe! Existe no arquivo unidades.csv
        # curso.id_unidade == id_unidade_designacao
        test_coordenador2 = test_coordenador2 or 'COORDENADOR DE CURSO' == funcao.atividade

    return grupo_chefes in grupos and test_coordenador1 and test_coordenador2


def docente_existe(usuario):
    """
    Verifica se na instância de Usuário existe um Docente relacionado.
    :param usuario: O usuário autenticado.
    :return: True se existir um Docente relacionado.
    """
    try:
        docente = usuario.docente
        return docente is not None
    except ObjectDoesNotExist:
        return False


def atualizar_solicitacao(request, pk):
    usuario = request.user
    if not discente_existe(usuario):
        messages.error(request, 'Não há um discente relacionado ao usuário.')
        return redirecionar(request)

    resultado, created = solicitacao_incluir(usuario, pk)

    if created:
        messages.success(request, 'Solicitação de Interesse na Turma ' +
                         str(resultado.turma) + ' cadastrada com sucesso.')
    else:
        messages.error(request, 'Já existe Solicitação de Interesse na Turma ' +
                       str(resultado.turma) + '.')

    return redirecionar(request)


def discente_existe(usuario):
    """
    Verifica se na instância de Usuário existe um Discente relacionado.
    :param usuario: O usuário autenticado.
    :return: True se existir um Docente relacionado.
    """
    try:
        discente = usuario.discente
        return discente is not None
    except ObjectDoesNotExist:
        return False


def discente_grade_horarios(request, discente):

    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')

    turmas = SolicitacaoTurma.objects.filter(solicitador=discente, turma__ano=ano,
                                             turma__periodo=periodo).select_related('turma')

    turmas_por_horario = carrega_turmas_por_horario(turmas)

    return turmas_por_horario


def carrega_turmas_por_horario(turmas):
    """
    Carrega uma lista com 16 posições representando os 16 períodos de 50 min de aulas em todos os turnos.
    Cada posição contém outra lista de 5 posições representando os dias da semana.
    :param turmas: Uma lista de Turmas ou Sugestões de Turma.
    :return: Uma lista bidimensional representando a grade de horários com a lista de turmas
    em cada horário.
    """
    tt = []
    tt.extend(carrega_horario_turmas_por_turno(turmas, 'M'))
    tt.extend(carrega_horario_turmas_por_turno(turmas, 'T'))
    tt.extend(carrega_horario_turmas_por_turno(turmas, 'N'))
    return tt


def carrega_horario_turmas_por_turno(turmas, turno):
    """
    Carrega uma lista com 16 posições representando os 16 períodos de 50 min de aulas para um turno.
    Cada posição contém outra lista de 5 posições representando os dias da semana.
    :param turmas: Uma lista de Turmas ou Sugestões de Turma.
    :param turno: Turno selecionado entre as opções M, T e N.
    :return: Uma lista bidimensional representando a grade de horários com a lista de turmas
    em cada horário.
    """
    tt = []
    n = 7
    if turno == 'N':
        n = 5

    for i in range(1, n):
        horarios = Horario.objects.filter(turno=turno, ordem=i).order_by('dia')
        turmas_horario = []
        for h in horarios:
            turmas_por_horario = []
            for t in turmas:
                horarios_solicitacao = list(t.turma.horarios.all())
                if horarios_solicitacao.__contains__(h):
                    turmas_por_horario.append(t.turma)
            th = TurmaHorario(h, turmas_por_horario)
            turmas_horario.append(th)
        tt.append(turmas_horario)
    return tt
