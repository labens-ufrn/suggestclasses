import logging
from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from core.bo.docente import get_funcao_by_siape
from core.bo.turma import atualiza_semestres, carrega_sugestao_turmas, carrega_turmas_horario
from core.config.config import get_config
from core.forms import SugestaoTurmaForm
from core.models import SugestaoTurma
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
        'semestres_atual': semestres,
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
            carregar_dados(request, sugestao_turma)
            if not verificar_existencia(request, form_sugestao, sugestao_turma):
                sugestao_turma.save()
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


def carregar_dados(request, sugestao_turma):
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')

    sugestao_turma.tipo = 'REGULAR'
    sugestao_turma.ano = ano
    sugestao_turma.periodo = periodo
    sugestao_turma.campus_turma = sugestao_turma.local.campus
    sugestao_turma.criador = request.user
    sugestao_turma.total_solicitacoes = 0


def verificar_existencia(request, form_sugestao, sugestao_turma):
    sugestoes = SugestaoTurma.objects.filter(
        codigo_turma=sugestao_turma.codigo_turma,
        componente=sugestao_turma.componente,
        ano=sugestao_turma.ano,
        periodo=sugestao_turma.periodo).values('codigo_turma')
    if sugestoes.exists():
        sugestoes = SugestaoTurma.objects.filter(
            componente=sugestao_turma.componente,
            ano=sugestao_turma.ano,
            periodo=sugestao_turma.periodo).values('codigo_turma')
        codigos_str = criar_string(sugestoes)
        form_sugestao.add_error('codigo_turma',
                                'Os seguintes códigos já foram utilizados: ' + codigos_str)
        return True
    return False


def criar_string(sugestoes):
    str_result = ''
    tam = len(sugestoes)
    for index, s in enumerate(sugestoes, start=1):
        str_result += s['codigo_turma']
        if tam > 1 and index < tam:
            str_result += ', '
    str_result += '.'
    return str_result


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_editar(request, pk, estrutura, template_name='core/sugestao/editar.html'):
    sugestao = get_object_or_404(SugestaoTurma, pk=pk)
    if not verificar_permissoes(request, sugestao, estrutura):
        messages.error(request, 'Você não tem permissão de Editar esta Sugestão de Turma.')
        return redirecionar(request)
    form = SugestaoTurmaForm(request.POST or None, instance=sugestao, estrutura=estrutura)
    if form.is_valid():
        form.save()
        messages.success(request, 'Sugestão de Turma alterada com sucesso.')
        return redirecionar(request)
    else:
        messages.error(request, form.errors)
    return render(request, template_name, {'form': form})


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
