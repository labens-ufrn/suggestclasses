import io
import logging
from random import sample
from typing import List

import matplotlib.pyplot as plt
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import DetailView
from matplotlib.backends.backend_agg import FigureCanvasAgg

from core.models import Curso, ComponenteCurricular, EstruturaCurricular, SugestaoTurma, Sala, Docente, Turma, \
    SolicitacaoTurma
from core.config.config import get_config
from core.visoes.flow_view import flow_horizontal, flow_opcionais, carrega_context_flow_list
from .bo.curso import get_cursos
from .bo.discentes import get_discentes, get_discentes_ativos
from .bo.docente import get_docentes, carrega_turmas_por_horario
from .bo.sala import get_salas
from .bo.sevices import get_oc_by_semestre, get_ch_by_semestre, get_estrutura_direito, get_estrutura_matematica, \
    get_estrutura_pedagogia, get_estrutura_administracao, get_estrutura_turismo, get_estrutura_letras_portugues, \
    get_estrutura_letras_espanhol, get_estrutura_letras_ingles
from .bo.sistemas import get_estrutura_sistemas, get_estrutura_sistemas_dct
from .dao.centro_dao import get_ceres
from .dao.componente_dao import get_componentes_by_depto, get_componentes_curriculares
from .dao.departamento_dao import get_departamentos
from .filters import SalaFilter, DocenteFilter
from .forms import CadastroUsuarioForm
from .models import Horario
from .visoes.suggest_view import sugestao_grade_horarios, sugestao_manter, sugestao_incluir, sugestao_editar, \
    redirecionar, sugestao_deletar, atualizar_solicitacao, discente_existe, docente_existe, criar_string, \
    discente_grade_horarios, solicitacao_discente_deletar, get_solicitacoes, docente_grade_horarios
from .visoes.turma_view import turmas_grade
from .visoes.user_view import criar_usuario, autenticar_logar

logger = logging.getLogger('suggestclasses.logger')
config = get_config()


def index(request):
    """
        View para o Home (Tela Inicial).
    :param request: Uma requisição http.
    :return: Um response com dados sobre o CERES/UFRN.
    """
    ceres = get_ceres()
    departamentos = get_departamentos()
    cursos = get_cursos()
    componentes = get_componentes_curriculares()
    docentes = get_docentes()
    discentes = get_discentes()
    discentes_ativos = get_discentes_ativos()

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
    ceres = get_ceres()
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
    ceres = get_ceres()
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
    departamentos = get_departamentos()

    context = {
        'departamentos': departamentos
    }

    return render(request, 'core/departamento/list.html', context)


def curso_list(request):
    """
            Lista todos os componentes curriculares.
    """
    cursos = Curso.objects.all()

    context = {
        'cursos': cursos
    }

    return render(request, 'core/curso/list.html', context)


def componente_list(request):
    """
        Lista todos os componentes curriculares.
    """
    componentes = ComponenteCurricular.objects.all()

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
    docentes = get_docentes()
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


def flow_dir(request):
    dir_ec = get_estrutura_direito()
    link_opcionais = '/core/flow/dir/opcionais'
    return flow_horizontal(request, dir_ec, link_opcionais)


def flow_dir_op(request):
    dir_ec = get_estrutura_direito()
    return flow_opcionais(request, dir_ec)


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
    dir_flow = get_estrutura_direito()
    bsi_flow = get_estrutura_sistemas_dct()
    ped_flow = get_estrutura_pedagogia()
    mat_flow = get_estrutura_matematica()
    adm_flow = get_estrutura_administracao()
    tur_flow = get_estrutura_turismo()
    let_por_flow = get_estrutura_letras_portugues()
    let_esp_flow = get_estrutura_letras_espanhol()
    let_ing_flow = get_estrutura_letras_ingles()

    context = {
        'dir_flow': dir_flow,
        'mat_flow': mat_flow,
        'ped_flow': ped_flow,
        'bsi_flow': bsi_flow,
        'adm_flow': adm_flow,
        'tur_flow': tur_flow,
        'let_por_flow': let_por_flow,
        'let_esp_flow': let_esp_flow,
        'let_ing_flow': let_ing_flow,
    }
    return render(request, 'core/turmas/list.html', context)


class TurmaDetailView(DetailView):
    model = Turma
    template_name = 'core/turmas/detalhar.html'


def turmas_dir(request):
    dir_ddir = get_estrutura_direito()
    turmas_list_link = '/core/turmas/dir'
    return turmas_grade(request, dir_ddir, turmas_list_link)


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
    dir_flow = get_estrutura_direito()
    bsi_flow = get_estrutura_sistemas_dct()
    ped_flow = get_estrutura_pedagogia()
    mat_flow = get_estrutura_matematica()
    adm_flow = get_estrutura_administracao()
    tur_flow = get_estrutura_turismo()
    let_por_flow = get_estrutura_letras_portugues()
    let_esp_flow = get_estrutura_letras_espanhol()
    let_ing_flow = get_estrutura_letras_ingles()

    context = {
        'dir_flow': dir_flow,
        'mat_flow': mat_flow,
        'ped_flow': ped_flow,
        'bsi_flow': bsi_flow,
        'adm_flow': adm_flow,
        'tur_flow': tur_flow,
        'let_por_flow': let_por_flow,
        'let_esp_flow': let_esp_flow,
        'let_ing_flow': let_ing_flow,
    }
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


@login_required(login_url='/accounts/login')
def profile(request, username):
    ano_periodo_atual = config.get('PeriodoAtual', 'ano_periodo')
    ano_atual = config.get('PeriodoAtual', 'ano')
    periodo_atual = config.get('PeriodoAtual', 'periodo')

    ano_periodo_seguinte = config.get('PeriodoSeguinte', 'ano_periodo')
    ano_seguinte = config.get('PeriodoSeguinte', 'ano')
    periodo_seguinte = config.get('PeriodoSeguinte', 'periodo')
    usuario = User.objects.get(username=username)

    if request.user != usuario:
        messages.error(request, 'Você não tem permissão de visualizar esse Perfil.')
        return redirecionar(request)

    horarios_atual = None
    horarios = None
    semestres = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    solicitacao_list = None

    if discente_existe(usuario):
        perfil = usuario.discente
        perfil_link = 'core/usuario/profile_discente.html'
        grupos = criar_string(usuario.groups.all())
        horarios = discente_grade_horarios(perfil, ano_seguinte, periodo_seguinte)
        solicitacao_list = get_solicitacoes(perfil, ano_seguinte, periodo_seguinte)
    elif docente_existe(usuario):
        perfil = usuario.docente
        perfil_link = 'core/usuario/profile_docente.html'
        grupos = criar_string(usuario.groups.all())
        horarios_atual = carrega_turmas_por_horario(perfil, ano_atual, periodo_atual)
        horarios = docente_grade_horarios(perfil, ano_seguinte, periodo_seguinte, semestres)
    else:
        perfil = None
        perfil_link = 'core/usuario/profile.html'
        grupos = criar_string(usuario.groups.all())

    context = {
        'usuario': usuario,
        'grupos': grupos,
        'perfil': perfil,
        'horarios_atual': horarios_atual,
        'horarios': horarios,
        'ano_periodo_atual': ano_periodo_atual,
        'ano_periodo': ano_periodo_seguinte,
        'solicitacao_deletar_link': 'solicitacao_deletar',
        'solicitacao_list': solicitacao_list,
    }

    return render(request, perfil_link, context)


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
