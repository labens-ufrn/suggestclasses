from core.bo.historico import listar_historicos_by_discente
import io
import logging
from random import sample
from typing import List
from django.db.models.expressions import OuterRef, Subquery

import matplotlib.pyplot as plt
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import DetailView
from matplotlib.backends.backend_agg import FigureCanvasAgg

from core.config.config import get_config
from core.models import Curso, ComponenteCurricular, EstruturaCurricular, SugestaoTurma, Sala, Docente, Turma, \
    SolicitacaoTurma, Enquete, VotoTurma
from core.visoes.flow_view import flow_horizontal, flow_opcionais, carrega_context_flow_list
from .bo.curso import get_cursos, get_cursos_by_centro
from .bo.discentes import get_discentes, get_discentes_ativos, get_discentes_by_centro, get_qtd_discentes_ativos
from .bo.docente import get_docentes, carrega_turmas_por_horario, get_docentes_by_centro
from .bo.enquetes import get_enquetes, get_enquetes_por_curso
from .bo.periodos import get_periodo_planejado, get_periodo_ativo
from .bo.sala import get_salas
from .bo.sevices import get_estrutura_direito, get_estrutura_matematica, \
    get_estrutura_pedagogia, get_estrutura_administracao, get_estrutura_turismo, get_estrutura_letras_portugues, \
    get_estrutura_letras_espanhol, get_estrutura_letras_ingles, get_estrutura_contabeis, \
    get_estrutura_historia_licenciatura, get_estrutura_historia_bacharelado, get_estrutura_geografia_bacharelado, \
    get_estrutura_geografia_licenciatura
from .bo.sistemas import get_estrutura_sistemas_dct
from .dao.centro_dao import get_ceres
from .dao.componente_dao import get_cc_by_centro, get_componentes_by_depto, get_componentes_curriculares
from .dao.departamento_dao import get_departamentos, get_deptos_by_centro
from .filters import SalaFilter, DocenteFilter, EnqueteFilter
from .forms import CadastroUsuarioForm
from .models import Horario, OrganizacaoCurricular
from .visoes.enquete_view import enquete_voto_view, enquete_deletar_voto_discente, get_qtd_votantes, get_qtd_abstencao, \
    enquete_detalhar_voto_view
from .visoes.suggest_view import sugestao_grade_horarios, sugestao_manter, sugestao_incluir, sugestao_editar, \
    redirecionar, sugestao_deletar, atualizar_solicitacao, discente_existe, docente_existe, criar_string, \
    discente_grade_horarios, solicitacao_discente_deletar, get_solicitacoes, docente_grade_horarios
from .visoes.turma_view import turmas_grade
from .visoes.user_view import criar_usuario, autenticar_logar

logger = logging.getLogger('suggestclasses.logger')
config = get_config()
ceres = get_ceres()

def index(request):
    """
    View para o Home (Tela Inicial).
    :param request: Uma requisição http.
    :return: Um response com dados sobre o CERES/UFRN.
    """
    departamentos = get_deptos_by_centro(centro=ceres)
    cursos = get_cursos_by_centro(ceres)
    componentes = get_cc_by_centro(ceres)
    docentes = get_docentes_by_centro(ceres)
    discentes = get_discentes_by_centro(ceres)
    discentes_ativos = get_discentes_ativos(centro=ceres)

    context = {
        'ceres': ceres,
        'departamentos': departamentos,
        'docentes': docentes,
        'cursos': cursos,
        'componentes': componentes,
        'discentes': discentes,
        'discentes_ativos': discentes_ativos,
    }

    return render(request, 'core/home.html', context)


def sobre(request):
    context = {
        'ceres': ceres,
    }
    return render(request, 'core/sobre.html', context)


@login_required(login_url='/accounts/login')
def dashboard(request):
    """
        View index para o Dashboard.
    :param request: Requisição do http.
    :return: retorna um HttpResponse
    """
    departamentos = get_departamentos()
    estruturas = EstruturaCurricular.objects.all()

    cursos = Curso.objects.all()
    componentes = get_componentes_curriculares()

    componentes_by_depto = []
    headers: List[str] = []

    for d in departamentos:
        headers.append(d.sigla)
        componentes_by_depto.append(get_componentes_by_depto(d))

    template = loader.get_template('core/dashboard.html')

    context = {
        'ceres': ceres,
        'departamentos': departamentos,
        'cursos': cursos,
        'componentes': componentes,
        'estruturas': estruturas,
        'headers': headers,
        'componentes_by_depto': componentes_by_depto,
    }
    return HttpResponse(template.render(context, request))


def detail(request, horario_id):
    return HttpResponse("You're looking at Horario %s." % horario_id)


def curso_detail(request, curso_id):
    curso = Curso.objects.get(pk=curso_id)
    return HttpResponse("You're looking at Curso %s." % curso)


def horarios_list(request):
    horario_list = Horario.objects.all()
    horarios = []

    for i in range(1, 7):
        horarios.append(Horario.objects.filter(ordem=i, turno='M').order_by('dia'))

    for i in range(1, 7):
        horarios.append(Horario.objects.filter(ordem=i, turno='T').order_by('dia'))

    for i in range(1, 5):
        horarios.append(Horario.objects.filter(ordem=i, turno='N').order_by('dia'))

    context = {
        'horario_list': horario_list,
        'horarios': horarios
    }

    return render(request, 'core/list.html', context)


def departamento_list(request):
    """
            Lista todos os componentes curriculares.
    """
    departamentos = get_deptos_by_centro(ceres)

    context = {
        'departamentos': departamentos
    }

    return render(request, 'core/departamento/list.html', context)


def curso_list(request):
    """
            Lista todos os componentes curriculares.
    """
    cursos = get_cursos_by_centro(ceres)

    context = {
        'cursos': cursos
    }

    return render(request, 'core/curso/list.html', context)


def componente_list(request):
    """
        Lista todos os componentes curriculares.
    """
    componentes = get_cc_by_centro(ceres)

    context = {
        'componentes': componentes
    }

    return render(request, 'core/componente/list.html', context)


class ComponenteDetailView(DetailView):
    model = ComponenteCurricular
    template_name = 'core/componente/detalhar.html'


class DocenteDetailView(DetailView):
    model = Docente
    template_name = 'core/docente/detalhar.html'


def curriculo_list(request):
    estruturas = EstruturaCurricular.objects.all()

    context = {
        'estruturas': estruturas
    }

    return render(request, 'core/curriculo/list.html', context)


def docentes_list(request):
    """
            Lista todas os docentes do centro.
    """
    docentes = get_docentes_by_centro(ceres)
    docente_filter = DocenteFilter(request.GET, queryset=docentes)
    context = {
        'filter': docente_filter
    }

    return render(request, 'core/docente/list.html', context)


def sala_list(request):
    """
            Lista todas as salas do centro.
    """
    salas = Sala.objects.all()

    context = {
        'salas': salas
    }

    return render(request, 'core/sala/list.html', context)


def flow_list(request):
    """
    Lista todas as Estruturas Curriculares do centro CERES.
    """
    context = carrega_context_flow_list()

    return render(request, 'core/flow/list.html', context)


def flow_bsi_1b_h(request):
    bsi_ec = get_estrutura_sistemas_dct()
    link_opcionais = '/core/flow/bsi/opcionais'
    return flow_horizontal(request, bsi_ec, link_opcionais)


def flow_bsi_op(request):
    bsi_ec = get_estrutura_sistemas_dct()
    return flow_opcionais(request, bsi_ec)


def flow_cont(request):
    contaveis_ec = get_estrutura_contabeis()
    link_opcionais = '/core/flow/cont/opcionais'
    return flow_horizontal(request, contaveis_ec, link_opcionais)


def flow_cont_op(request):
    contaveis_ec = get_estrutura_contabeis()
    return flow_opcionais(request, contaveis_ec)


def flow_dir(request):
    dir_ec = get_estrutura_direito()
    link_opcionais = '/core/flow/dir/opcionais'
    return flow_horizontal(request, dir_ec, link_opcionais)


def flow_dir_op(request):
    dir_ec = get_estrutura_direito()
    return flow_opcionais(request, dir_ec)


def flow_his_lic(request):
    his_lic_ec = get_estrutura_historia_licenciatura()
    link_opcionais = '/core/flow/his-lic/opcionais'
    return flow_horizontal(request, his_lic_ec, link_opcionais)


def flow_his_lic_op(request):
    his_lic_ec = get_estrutura_historia_licenciatura()
    return flow_opcionais(request, his_lic_ec)


def flow_his_bac(request):
    his_bac_ec = get_estrutura_historia_bacharelado()
    link_opcionais = '/core/flow/his-bac/opcionais'
    return flow_horizontal(request, his_bac_ec, link_opcionais)


def flow_his_bac_op(request):
    his_bac_ec = get_estrutura_historia_bacharelado()
    return flow_opcionais(request, his_bac_ec)


def flow_geo_lic(request):
    geo_lic_ec = get_estrutura_geografia_licenciatura()
    link_opcionais = '/core/flow/geo-lic/opcionais'
    return flow_horizontal(request, geo_lic_ec, link_opcionais)


def flow_geo_lic_op(request):
    geo_lic_ec = get_estrutura_geografia_licenciatura()
    return flow_opcionais(request, geo_lic_ec)


def flow_geo_bac(request):
    geo_bac_ec = get_estrutura_geografia_bacharelado()
    link_opcionais = '/core/flow/geo-bac/opcionais'
    return flow_horizontal(request, geo_bac_ec, link_opcionais)


def flow_geo_bac_op(request):
    geo_bac_ec = get_estrutura_geografia_bacharelado()
    return flow_opcionais(request, geo_bac_ec)


def flow_let_por(request):
    let_por_ec = get_estrutura_letras_portugues()
    link_opcionais = '/core/flow/let-por/opcionais'
    return flow_horizontal(request, let_por_ec, link_opcionais)


def flow_let_por_op(request):
    let_por_ec = get_estrutura_letras_portugues()
    return flow_opcionais(request, let_por_ec)


def flow_let_esp(request):
    let_esp_ec = get_estrutura_letras_espanhol()
    link_opcionais = '/core/flow/let-esp/opcionais'
    return flow_horizontal(request, let_esp_ec, link_opcionais)


def flow_let_esp_op(request):
    let_esp_ec = get_estrutura_letras_espanhol()
    return flow_opcionais(request, let_esp_ec)


def flow_let_ing(request):
    let_ing_ec = get_estrutura_letras_ingles()
    link_opcionais = '/core/flow/let-ing/opcionais'
    return flow_horizontal(request, let_ing_ec, link_opcionais)


def flow_let_ing_op(request):
    let_ing_ec = get_estrutura_letras_ingles()
    return flow_opcionais(request, let_ing_ec)


def flow_mat_h(request):
    mat_ec = get_estrutura_matematica()
    link_opcionais = '/core/flow/mat/opcionais'
    return flow_horizontal(request, mat_ec, link_opcionais)


def flow_mat_op(request):
    mat_ec = get_estrutura_matematica()
    return flow_opcionais(request, mat_ec)


def flow_ped_h(request):
    ped_ec = get_estrutura_pedagogia()
    link_opcionais = '/core/flow/ped/opcionais'
    return flow_horizontal(request, ped_ec, link_opcionais)


def flow_ped_op(request):
    ped_ec = get_estrutura_pedagogia()
    return flow_opcionais(request, ped_ec)


def flow_adm(request):
    adm_ec = get_estrutura_administracao()
    link_opcionais = '/core/flow/adm/opcionais'
    return flow_horizontal(request, adm_ec, link_opcionais)


def flow_adm_op(request):
    adm_ec = get_estrutura_administracao()
    return flow_opcionais(request, adm_ec)


def flow_tur(request):
    tur_ec = get_estrutura_turismo()
    link_opcionais = '/core/flow/tur/opcionais'
    return flow_horizontal(request, tur_ec, link_opcionais)


def flow_tur_op(request):
    tur_ec = get_estrutura_turismo()
    return flow_opcionais(request, tur_ec)


def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = CadastroUsuarioForm(request.POST)
        if form_usuario.is_valid():
            try:
                criar_usuario(request, form_usuario)
                autenticar_logar(request, form_usuario)
                messages.success(request, 'Usuário cadastrado com sucesso.')
                return redirect('index')
            except ValidationError as e:
                form_usuario.add_error(None, e)
        else:
            messages.error(request, 'O formulário contém dados inválidos!')
    else:
        form_usuario = CadastroUsuarioForm()
    return render(request, 'core/usuario/cadastro.html', {'form_usuario': form_usuario})


def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            messages.success(request, 'Usuário logado com sucesso.')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao logar usuário.')
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'core/usuario/login.html', {'form_login': form_login})


@login_required(login_url='/core/usuario/logar')
def deslogar_usuario(request):
    logout(request)
    messages.success(request, 'Usuário deslogado com sucesso.')
    return redirect('index')


@login_required(login_url='/core/usuario/logar')
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Usuário atualizado com sucesso.')
            return redirect('index')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'core/usuario/alterar_senha.html', {'form_senha': form_senha})


def turmas_list(request):
    """
        Lista todas as Turmas do centro CERES.
    """
    context = carrega_context_flow_list()
    return render(request, 'core/turmas/list.html', context)


class TurmaDetailView(DetailView):
    model = Turma
    template_name = 'core/turmas/detalhar.html'


def turmas_cont(request):
    cont_ec = get_estrutura_contabeis()
    turmas_list_link = '/core/turmas/cont'
    return turmas_grade(request, cont_ec, turmas_list_link)


def turmas_dir(request):
    dir_ddir = get_estrutura_direito()
    turmas_list_link = '/core/turmas/dir'
    return turmas_grade(request, dir_ddir, turmas_list_link)


def turmas_his_bac(request):
    his_bac_ec = get_estrutura_historia_bacharelado()
    turmas_list_link = '/core/turmas/his-bac'
    return turmas_grade(request, his_bac_ec, turmas_list_link)


def turmas_his_lic(request):
    his_lic_ec = get_estrutura_historia_licenciatura()
    turmas_list_link = '/core/turmas/his-lic'
    return turmas_grade(request, his_lic_ec, turmas_list_link)


def turmas_geo_bac(request):
    geo_bac_ec = get_estrutura_geografia_bacharelado()
    turmas_list_link = '/core/turmas/geo-bac'
    return turmas_grade(request, geo_bac_ec, turmas_list_link)


def turmas_geo_lic(request):
    geo_lic_ec = get_estrutura_geografia_licenciatura()
    turmas_list_link = '/core/turmas/geo-lic'
    return turmas_grade(request, geo_lic_ec, turmas_list_link)


def turmas_let_esp(request):
    let_esp_ec = get_estrutura_letras_espanhol()
    turmas_list_link = '/core/turmas/let-esp'
    return turmas_grade(request, let_esp_ec, turmas_list_link)


def turmas_let_por(request):
    let_por_ec = get_estrutura_letras_portugues()
    turmas_list_link = '/core/turmas/let-por'
    return turmas_grade(request, let_por_ec, turmas_list_link)


def turmas_let_ing(request):
    let_ing_ec = get_estrutura_letras_ingles()
    turmas_list_link = '/core/turmas/let-ing'
    return turmas_grade(request, let_ing_ec, turmas_list_link)


def turmas_mat(request):
    mat_dcea = get_estrutura_matematica()
    turmas_list_link = '/core/turmas/mat'
    return turmas_grade(request, mat_dcea, turmas_list_link)


def turmas_bsi(request):
    bsi_dct = get_estrutura_sistemas_dct()
    turmas_list_link = '/core/turmas/bsi'
    return turmas_grade(request, bsi_dct, turmas_list_link)


def turmas_ped(request):
    ped_deduc = get_estrutura_pedagogia()
    turmas_list_link = '/core/turmas/ped'
    return turmas_grade(request, ped_deduc, turmas_list_link)


def turmas_adm(request):
    adm_csh = get_estrutura_administracao()
    turmas_list_link = '/core/turmas/adm'
    return turmas_grade(request, adm_csh, turmas_list_link)


def turmas_tur(request):
    tur_csh = get_estrutura_turismo()
    turmas_list_link = '/core/turmas/tur'
    return turmas_grade(request, tur_csh, turmas_list_link)


def sugestao_list(request):
    """
    Tela para Listar os Curso com possibilidade de cadastrar Sugestões de Turmas.
    """
    context = carrega_context_flow_list()
    return render(request, 'core/sugestao/list.html', context)


class SugestaoTurmaDetailView(DetailView):
    model = SugestaoTurma
    template_name = 'core/sugestao/detalhar.html'


@permission_required("core.add_solicitacaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_solicitar(request, pk):
    return atualizar_solicitacao(request, pk)


@login_required(login_url='/accounts/login')
def solicitacao_turma_listar(request, pk):

    turma = SugestaoTurma.objects.get(pk=pk)
    solicitacoes = SolicitacaoTurma.objects.filter(turma=turma).order_by('criada_em', 'solicitador__nome_curso')

    context = {
        'turma': turma,
        'solicitacoes': solicitacoes,
    }

    return render(request, 'core/sugestao/solicitacao_listar.html', context)


@permission_required("core.delete_solicitacaoturma", login_url='/core/usuario/logar', raise_exception=True)
def solicitacao_deletar(request, pk):
    return solicitacao_discente_deletar(request, pk)


def sugestao_adm_list(request):
    adm_csh = get_estrutura_administracao()
    sugestao_incluir_link = '/core/sugestao/adm/incluir'
    sugestao_manter_link = '/core/sugestao/adm/manter'
    sugestao_list_link = '/core/sugestao/adm/list'
    return sugestao_grade_horarios(request, adm_csh, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_adm_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Administração - Currais Novos.
    """
    adm_csh = get_estrutura_administracao()
    sugestao_incluir_link = '/core/sugestao/adm/incluir'
    sugestao_editar_link = 'sugestao_adm_editar'
    sugestao_deletar_link = 'sugestao_adm_deletar'
    sugestao_grade_link = '/core/sugestao/adm/list'
    return sugestao_manter(request, adm_csh, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_adm_incluir(request):
    adm_csh = get_estrutura_administracao()
    sugestao_manter_link = '/core/sugestao/adm/manter'
    return sugestao_incluir(request, adm_csh, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_adm_editar(request, pk):
    adm_csh = get_estrutura_administracao()
    return sugestao_editar(request, pk, estrutura=adm_csh)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_adm_deletar(request, pk):
    adm_csh = get_estrutura_administracao()
    return sugestao_deletar(request, pk, estrutura=adm_csh)


def sugestao_dir_list(request):
    dir_ddir = get_estrutura_direito()
    sugestao_incluir_link = '/core/sugestao/dir/incluir'
    sugestao_manter_link = '/core/sugestao/dir/manter'
    sugestao_list_link = '/core/sugestao/dir/list'
    return sugestao_grade_horarios(request, dir_ddir, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_dir_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Direito.
    """
    dir_ddir = get_estrutura_direito()
    sugestao_incluir_link = '/core/sugestao/dir/incluir'
    sugestao_editar_link = 'sugestao_dir_editar'
    sugestao_deletar_link = 'sugestao_dir_deletar'
    sugestao_grade_link = '/core/sugestao/dir/list'
    return sugestao_manter(request, dir_ddir, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_dir_incluir(request):
    dir_ddir = get_estrutura_direito()
    sugestao_manter_link = '/core/sugestao/dir/manter'
    return sugestao_incluir(request, dir_ddir, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_dir_editar(request, pk):
    dir_ddir = get_estrutura_direito()
    return sugestao_editar(request, pk, estrutura=dir_ddir)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_dir_deletar(request, pk):
    dir_ddir = get_estrutura_direito()
    return sugestao_deletar(request, pk, estrutura=dir_ddir)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_mat_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Matemática.
    """
    mat_dcea = get_estrutura_matematica()
    sugestao_incluir_link = '/core/sugestao/mat/incluir'
    sugestao_editar_link = 'sugestao_mat_editar'
    sugestao_deletar_link = 'sugestao_mat_deletar'
    sugestao_grade_link = '/core/sugestao/mat/list'
    return sugestao_manter(request, mat_dcea, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_mat_incluir(request):
    mat_dcea = get_estrutura_matematica()
    sugestao_manter_link = '/core/sugestao/mat/manter'
    return sugestao_incluir(request, mat_dcea, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_mat_editar(request, pk):
    mat_dcea = get_estrutura_matematica()
    return sugestao_editar(request, pk, estrutura=mat_dcea)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_mat_deletar(request, pk):
    mat_dcea = get_estrutura_matematica()
    return sugestao_deletar(request, pk, estrutura=mat_dcea)


def sugestao_mat_list(request):
    mat_dcea = get_estrutura_matematica()
    sugestao_incluir_link = '/core/sugestao/mat/incluir'
    sugestao_manter_link = '/core/sugestao/mat/manter'
    sugestao_list_link = '/core/sugestao/mat/list'
    return sugestao_grade_horarios(request, mat_dcea, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_bsi_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Sistemas de Informação.
    """
    bsi_dct = get_estrutura_sistemas_dct()
    sugestao_incluir_link = '/core/sugestao/bsi/incluir'
    sugestao_editar_link = 'sugestao_bsi_editar'
    sugestao_deletar_link = 'sugestao_bsi_deletar'
    sugestao_grade_link = '/core/sugestao/bsi/list'
    return sugestao_manter(request, bsi_dct, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_bsi_incluir(request):
    bsi_dct = get_estrutura_sistemas_dct()
    sugestao_manter_link = '/core/sugestao/bsi/manter'
    return sugestao_incluir(request, bsi_dct, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_bsi_editar(request, pk):
    bsi_dct = get_estrutura_sistemas_dct()
    return sugestao_editar(request, pk, estrutura=bsi_dct)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_bsi_deletar(request, pk):
    bsi_dct = get_estrutura_sistemas_dct()
    return sugestao_deletar(request, pk, estrutura=bsi_dct)


def sugestao_bsi_list(request):
    bsi_dct = get_estrutura_sistemas_dct()
    sugestao_incluir_link = '/core/sugestao/bsi/incluir'
    sugestao_manter_link = '/core/sugestao/bsi/manter'
    sugestao_list_link = '/core/sugestao/bsi/list'
    return sugestao_grade_horarios(request, bsi_dct, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


def sugestao_ped_list(request):
    ped_deduc = get_estrutura_pedagogia()
    sugestao_incluir_link = '/core/sugestao/ped/incluir'
    sugestao_manter_link = '/core/sugestao/ped/manter'
    sugestao_list_link = '/core/sugestao/ped/list'
    return sugestao_grade_horarios(request, ped_deduc, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_ped_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Pedagogia.
    """
    ped_deduc = get_estrutura_pedagogia()
    sugestao_incluir_link = '/core/sugestao/ped/incluir'
    sugestao_editar_link = 'sugestao_ped_editar'
    sugestao_deletar_link = 'sugestao_ped_deletar'
    sugestao_grade_link = '/core/sugestao/ped/list'
    return sugestao_manter(request, ped_deduc, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_ped_incluir(request):
    ped_deduc = get_estrutura_pedagogia()
    sugestao_manter_link = '/core/sugestao/ped/manter'
    return sugestao_incluir(request, ped_deduc, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_ped_editar(request, pk):
    ped_deduc = get_estrutura_pedagogia()
    return sugestao_editar(request, pk, estrutura=ped_deduc)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_ped_deletar(request, pk):
    ped_deduc = get_estrutura_pedagogia()
    return sugestao_deletar(request, pk, estrutura=ped_deduc)


def sugestao_tur_list(request):
    tur_csh = get_estrutura_turismo()
    sugestao_incluir_link = '/core/sugestao/tur/incluir'
    sugestao_manter_link = '/core/sugestao/tur/manter'
    sugestao_list_link = '/core/sugestao/tur/list'
    return sugestao_grade_horarios(request, tur_csh, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_tur_manter(request):
    """
        Tela de Manter Sugestão de Turmas do Curso de Turismo - Currais Novos.
    """
    tur_csh = get_estrutura_turismo()
    sugestao_incluir_link = '/core/sugestao/tur/incluir'
    sugestao_editar_link = 'sugestao_tur_editar'
    sugestao_deletar_link = 'sugestao_tur_deletar'
    sugestao_grade_link = '/core/sugestao/tur/list'
    return sugestao_manter(request, tur_csh, sugestao_incluir_link, sugestao_grade_link,
                           sugestao_editar_link, sugestao_deletar_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_tur_incluir(request):
    tur_csh = get_estrutura_turismo()
    sugestao_manter_link = '/core/sugestao/tur/manter'
    return sugestao_incluir(request, tur_csh, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_tur_editar(request, pk):
    tur_csh = get_estrutura_turismo()
    return sugestao_editar(request, pk, estrutura=tur_csh)


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_tur_deletar(request, pk):
    tur_csh = get_estrutura_turismo()
    return sugestao_deletar(request, pk, estrutura=tur_csh)


def error_403(request, exception):
    logger.error('Você não tem permissão de acessar "' + request.path + '" 403 ',
                 exc_info=exception)
    messages.error(request, 'Você não tem permissão de acessar: ' + request.path)
    return redirecionar(request)


def search_salas(request):
    salas = get_salas()
    sala_filter = SalaFilter(request.GET, queryset=salas)
    return render(request, 'core/sala/list.html', {'filter': sala_filter})


class EnqueteDetailView(DetailView):
    model = Enquete
    template_name = 'core/enquetes/detalhar.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Subconsulta para saber o período do componente
        periodo_qs = OrganizacaoCurricular.objects.filter(
            estrutura__curso=self.object.curso,
            componente=OuterRef("componente__pk")
            )
        # Consulta com a totalização de votos por componente
        votos_por_componente = VotoTurma.objects\
            .filter(enquete=self.object, tipo=VotoTurma.VALIDO) \
            .values('componente__pk', 'componente__codigo', 'componente__nome') \
            .annotate(votos=Count('componente')) \
            .annotate(periodo=Subquery(periodo_qs.values('semestre')[:1])) \
            .order_by('-votos', 'componente__nome')
        context['votos_por_componente'] = votos_por_componente
        curso = self.object.curso
        if not self.object.qtd_discentes_ativos:
            self.object.qtd_discentes_ativos = get_qtd_discentes_ativos(curso)
            self.object.save()
        # qtd_ativos = get_qtd_discentes_ativos(curso)
        qtd_ativos = self.object.qtd_discentes_ativos
        qtd_votantes = get_qtd_votantes(self.object)
        qtd_abstencao = get_qtd_abstencao(self.object)
        context['discentes_ativos'] = qtd_ativos
        taxa = round((qtd_votantes / qtd_ativos) * 100.0, 2)
        taxa_abstencao = round((qtd_abstencao / qtd_ativos) * 100.0, 2)
        context['taxa_votacao'] = str(taxa) + '% (' + str(qtd_votantes) + ' discentes)'
        context['taxa_abstencao'] = str(taxa_abstencao) + '% (' + str(qtd_abstencao) + ' discentes)'

        return context


def search_enquetes(request):

    usuario = request.user
    if usuario.id is not None and discente_existe(usuario):
        discente = usuario.discente
        enquetes = get_enquetes_por_curso(discente.id_curso)
    else:
        enquetes = get_enquetes()
    enquete_filter = EnqueteFilter(request.GET, queryset=enquetes)
    return render(request, 'core/enquetes/list.html', {'filter': enquete_filter})


@permission_required("core.add_vototurma", login_url='/core/usuario/logar', raise_exception=True)
def enquete_votar(request, pk):
    return enquete_voto_view(request, pk)


@login_required(login_url='/accounts/login')
def enquete_detalhar_voto(request, pk):
    return enquete_detalhar_voto_view(request, pk)


@permission_required("core.add_vototurma", login_url='/core/usuario/logar', raise_exception=True)
def enquete_abstencao(request, pk):
    return enquete_voto_view(request, pk, abstencao=True)


@permission_required("core.delete_vototurma", login_url='/core/usuario/logar', raise_exception=True)
def enquete_deletar_voto(request, pk):
    return enquete_deletar_voto_discente(request, pk)


@login_required(login_url='/accounts/login')
def enquete_votos_listar(request, pk, cc_pk):

    enquete = Enquete.objects.get(pk=pk)
    componente = ComponenteCurricular.objects.get(pk=cc_pk)
    votos_componente = VotoTurma.objects.filter(enquete_id=pk, componente__pk=cc_pk)\
        .order_by('criado_em', 'discente__nome_discente')

    context = {
        'enquete': enquete,
        'componente': componente,
        'votos_componente': votos_componente,
    }

    return render(request, 'core/enquetes/votos_listar.html', context)




def plot(request):
    # Creamos los datos para representar en el gráfico
    x = range(1, 11)
    y = sample(range(20), len(x))

    # Creamos una figura y le dibujamos el gráfico
    f = plt.figure()

    # Creamos los ejes
    axes = f.add_axes([0.15, 0.15, 0.75, 0.75])  # [left, bottom, width, height]
    axes.plot(x, y)
    axes.set_xlabel("Eje X")
    axes.set_ylabel("Eje Y")
    axes.set_title("Mi gráfico dinámico")

    # Como enviaremos la imagen en bytes la guardaremos en un buffer
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')

    # Limpiamos la figura para liberar memoria
    f.clear()

    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))

    # Devolvemos la response
    return response
