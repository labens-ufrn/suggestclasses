import io
import logging
from random import sample
from typing import List
from urllib.parse import urlparse

import matplotlib.pyplot as plt
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views.generic import DetailView
from matplotlib.backends.backend_agg import FigureCanvasAgg

from core.models import Curso, ComponenteCurricular, EstruturaCurricular, SugestaoTurma, Sala, Docente, Turma
from core.visoes.flow_view import flow_horizontal, flow_opcionais
from mysite.settings import DOMAINS_WHITELIST
from .bo.curso import get_cursos
from .bo.discentes import get_discentes
from .bo.docente import get_docentes
from .bo.matematica import get_estrutura_matematica
from .bo.pedagogia import get_estrutura_pedagogia
from .bo.sala import get_salas
from .bo.sevices import get_oc_by_semestre, get_ch_by_semestre
from .bo.sistemas import get_estrutura_sistemas, get_estrutura_sistemas_dct
from .bo.turma import carrega_turmas, carrega_turmas_horario, \
    carrega_sugestao_turmas, atualiza_semestres, atualiza_ano_periodo
from .config.config import get_config
from .dao.centro_dao import get_ceres
from .dao.componente_dao import get_componentes_by_depto, get_componentes_curriculares
from .dao.departamento_dao import get_departamentos
from .forms import CadastroUsuarioForm, SugestaoTurmaForm
from .models import Horario
# Get an instance of a logger
from .visoes.suggest_view import sugestao_grade_horarios, sugestao_manter, sugestao_incluir
from .visoes.user_view import criar_usuario, autenticar_logar

logger = logging.getLogger('suggestclasses.logger')


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
    salas = get_salas()
    docentes = get_docentes()
    discentes = get_discentes()

    context = {
        'ceres': ceres,
        'departamentos': departamentos,
        'docentes': docentes,
        'cursos': cursos,
        'componentes': componentes,
        'salas': salas,
        'discentes': discentes,
    }

    return render(request, 'core/home.html', context)


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


def curriculo_list(request):
    estruturas = EstruturaCurricular.objects.all()

    context = {
        'estruturas': estruturas
    }

    return render(request, 'core/curriculo/list.html', context)


def docente_list(request):
    """
            Lista todas os docentes do centro.
    """
    docentes = Docente.objects.all()

    context = {
        'docentes': docentes
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
    bsi_flow_1a = get_estrutura_sistemas()
    bsi_flow_1b = get_estrutura_sistemas_dct()
    ped_flow = get_estrutura_pedagogia()
    mat_flow = get_estrutura_matematica()

    context = {
        'mat_flow': mat_flow,
        'ped_flow': ped_flow,
        'bsi_flow_1a': bsi_flow_1a,
        'bsi_flow_1b': bsi_flow_1b
    }

    return render(request, 'core/flow/list.html', context)


def flow_bsi(request):
    bsi_ec = get_estrutura_sistemas()

    bsi_oc_semestres = []
    bsi_ch_semestres = []
    bsi_oc_op = get_oc_by_semestre(bsi_ec, 0)

    headers: List[str] = []

    for s in range(1, 9):
        headers.append(f"{s}º Semestre")
        bsi_oc_semestres.append(get_oc_by_semestre(bsi_ec, s))
        bsi_ch_semestres.append(get_ch_by_semestre(bsi_ec, s))

    context = {
        'bsi_ec': bsi_ec,
        'headers': headers,
        'bsi_oc_semestres': bsi_oc_semestres,
        'bsi_oc_op': bsi_oc_op,
        'bsi_ch_semestres': bsi_ch_semestres,
    }

    return render(request, 'core/flow/bsi.html', context)


def flow_bsi_1b(request):
    bsi_ec = get_estrutura_sistemas_dct()

    bsi_oc_semestres = []
    bsi_ch_semestres = []
    bsi_oc_op = get_oc_by_semestre(bsi_ec, 0)

    headers: List[str] = []
    bsi_tam = []
    bsi_oc_max = 0
    for s in range(1, 9):
        oc = get_oc_by_semestre(bsi_ec, s)
        ch = get_ch_by_semestre(bsi_ec, s)

        headers.append(f"{s}º Semestre")
        tam = len(oc)
        bsi_tam.append(tam)
        bsi_oc_semestres.append(oc)
        bsi_ch_semestres.append(ch)

        if tam >= bsi_oc_max:
            bsi_oc_max = tam

    for i in range(0, len(bsi_tam)):
        bsi_tam[i] = bsi_oc_max - bsi_tam[i]

    context = {
        'bsi_ec': bsi_ec,
        'headers': headers,
        'bsi_oc_semestres': bsi_oc_semestres,
        'bsi_oc_op': bsi_oc_op,
        'bsi_tam': bsi_tam,
        'bsi_oc_max': bsi_oc_max,
        'bsi_ch_semestres': bsi_ch_semestres,
    }

    return render(request, 'core/flow/bsi-1b.html', context)


def flow_bsi_1b_h(request):
    bsi_ec = get_estrutura_sistemas_dct()
    link_opcionais = '/core/flow/bsi/opcionais'
    return flow_horizontal(request, bsi_ec, link_opcionais)


def flow_bsi_op(request):
    bsi_ec = get_estrutura_sistemas_dct()
    return flow_opcionais(request, bsi_ec)


def flow_mat_h(request):
    mat_ec = get_estrutura_matematica()
    link_opcionais = '/core/flow/mat/opcionais'
    return flow_horizontal(request, mat_ec, link_opcionais)


def flow_mat_op(request):
    mat_ec = get_estrutura_matematica()
    return flow_opcionais(request, mat_ec)


def flow_ped_op(request):
    ped_ec = get_estrutura_pedagogia()
    return flow_opcionais(request, ped_ec)


def flow_ped(request):
    ped_ec = get_estrutura_pedagogia()

    ped_oc_semestres = []
    ped_ch_semestres = []
    ped_oc_op = get_oc_by_semestre(ped_ec, 0)

    headers: List[str] = []

    for s in range(1, 9):
        headers.append(f"{s}º Semestre")
        ped_oc_semestres.append(get_oc_by_semestre(ped_ec, s))
        ped_ch_semestres.append(get_ch_by_semestre(ped_ec, s))

    context = {
        'ped_ec': ped_ec,
        'headers': headers,
        'ped_oc_semestres': ped_oc_semestres,
        'ped_oc_op': ped_oc_op,
        'ped_ch_semestres': ped_ch_semestres,
    }

    return render(request, 'core/flow/pedagogia.html', context)


def flow_ped_h(request):
    ped_ec = get_estrutura_pedagogia()
    link_opcionais = '/core/flow/ped/opcionais'
    return flow_horizontal(request, ped_ec, link_opcionais)


def flow_ped_op(request):
    ped_ec = get_estrutura_pedagogia()
    return flow_opcionais(request, ped_ec)


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


def turma_list(request):
    return render(request, 'core/turma/list.html')


def turma_bsi(request):
    bsi_dct = get_estrutura_sistemas_dct()

    semestres = request.GET.getlist('semestres')
    ano_periodo = request.GET.getlist('ano_periodo')

    turmas = carrega_turmas(bsi_dct, semestres, ano_periodo)

    tt = carrega_turmas_horario(turmas)

    periodo_selecionado = atualiza_ano_periodo(ano_periodo)
    semestres_selecionado = atualiza_semestres(semestres)

    context = {
        'tt': tt,
        'periodo_selecionado': periodo_selecionado[0],
        'semestres_selecionado': semestres_selecionado
    }

    return render(request, 'core/turma/bsi.html', context)


def turma_ped(request):
    ped_deduc = get_estrutura_pedagogia()

    semestres = request.GET.getlist('semestres')
    ano_periodo = request.GET.getlist('ano_periodo')

    turmas = carrega_turmas(ped_deduc, semestres, ano_periodo)

    tt = carrega_turmas_horario(turmas)

    periodo_selecionado = atualiza_ano_periodo(ano_periodo)
    semestres_selecionado = atualiza_semestres(semestres)

    context = {
        'tt': tt,
        'periodo_selecionado': periodo_selecionado[0],
        'semestres_selecionado': semestres_selecionado
    }

    return render(request, 'core/turma/ped.html', context)


def sugestao_list(request):
    return render(request, 'core/sugestao/list.html')


def sugestao_bsi_manter(request):
    """
            Lista todas as salas do centro.
    """
    bsi_dct = get_estrutura_sistemas_dct()
    # Todos os Semestres
    semestres = ['100']
    semestres = atualiza_semestres(semestres)

    config = get_config()
    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')
    st_list = carrega_sugestao_turmas(bsi_dct, semestres, ano, periodo)

    context = {
        'ano_periodo': ano_periodo,
        'sugestao_bsi_list': '/core/sugestao/bsi/list',
        'sugestao_list': st_list
    }

    return render(request, 'core/sugestao/bsi/manter.html', context)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_bsi_incluir(request):
    bsi = get_estrutura_sistemas_dct()
    config = get_config()
    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')
    if request.method == "POST":
        form_sugestao = SugestaoTurmaForm(request.POST, estrutura=bsi)
        if form_sugestao.is_valid():
            sugestao_turma = form_sugestao.save(commit=False)
            sugestao_turma.tipo = 'REGULAR'
            sugestao_turma.ano = ano
            sugestao_turma.periodo = periodo
            sugestao_turma.campus_turma = sugestao_turma.local.campus
            sugestao_turma.save()
            messages.success(request, 'Sugestão de Turma cadastrada com sucesso.')
            return redirect('/core/sugestao/bsi/manter')
        else:
            messages.error(request, form_sugestao.errors['__all__'])
    else:
        form_sugestao = SugestaoTurmaForm(estrutura=bsi)
        context = {
            'ano_periodo': ano_periodo,
            'estrutura': bsi,
            'form_sugestao': form_sugestao
        }
    return render(request, 'core/sugestao/bsi/incluir.html', context)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_bsi_editar(request, pk):
    bsi = get_estrutura_sistemas_dct()
    return edit(request, pk, estrutura=bsi)


def sugestao_bsi(request):
    bsi_dct = get_estrutura_sistemas_dct()

    semestres = request.GET.getlist('semestres')
    semestres = atualiza_semestres(semestres)
    config = get_config()
    ano_periodo = config.get('PeriodoSeguinte', 'ano_periodo')
    ano = config.get('PeriodoSeguinte', 'ano')
    periodo = config.get('PeriodoSeguinte', 'periodo')
    turmas = carrega_sugestao_turmas(bsi_dct, semestres, ano, periodo)

    tt = carrega_turmas_horario(turmas)

    context = {
        'tt': tt,
        'periodo_atual': ano_periodo,
        'semestres_atual': semestres
    }

    return render(request, 'core/sugestao/bsi/list.html', context)


def sugestao_ped(request):
    ped_deduc = get_estrutura_pedagogia()
    sugestao_incluir_link = '/core/sugestao/ped/incluir'
    sugestao_manter_link = '/core/sugestao/ped/manter'
    return sugestao_grade_horarios(request, ped_deduc, sugestao_incluir_link, sugestao_manter_link)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_ped_manter(request):
    ped_deduc = get_estrutura_pedagogia()
    sugestao_incluir_link = '/core/sugestao/ped/incluir'
    sugestao_grade_link = '/core/sugestao/ped/list'
    return sugestao_manter(request, ped_deduc, sugestao_incluir_link, sugestao_grade_link)


@permission_required("core.add_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_ped_incluir(request):
    ped = get_estrutura_pedagogia()
    sugestao_manter_link = '/core/sugestao/ped/manter'
    return sugestao_incluir(request, ped, sugestao_manter_link)


class TurmaDetailView(DetailView):
    model = Turma
    template_name = 'core/turma/detalhar.html'


class SugestaoTurmaDetailView(DetailView):
    model = SugestaoTurma
    template_name = 'core/sugestao/detalhar.html'


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_ped_editar(request, pk):
    ped = get_estrutura_pedagogia()
    return edit(request, pk, estrutura=ped)


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def edit(request, pk, estrutura, template_name='core/sugestao/editar.html'):
    sugestao = get_object_or_404(SugestaoTurma, pk=pk)
    form = SugestaoTurmaForm(request.POST or None, instance=sugestao, estrutura=estrutura)
    if form.is_valid():
        form.save()
        messages.success(request, 'Sugestão de Turma alterada com sucesso.')
        return redirecionar(request)
    else:
        messages.error(request, form.errors)
    return render(request, template_name, {'form': form})


@permission_required("core.delete_sugestao_turma", login_url='/core/usuario/logar', raise_exception=True)
def delete(request, pk, template_name='core/sugestao/confirm_delete.html'):
    sugestao = get_object_or_404(SugestaoTurma, pk=pk)
    if request.method == 'POST':
        sugestao.delete()
        messages.success(request, 'Sugestão de Turma excluída com sucesso.')
        return redirecionar(request)
    return render(request, template_name, {'object': sugestao})


def error_403(request, exception):
    logger.error('Você não tem permissão de acessar "' + request.path + '" 403 ',
                 exc_info=exception)
    messages.error(request, 'Você não tem permissão de acessar: ' + request.path)
    return redirecionar(request)


def redirecionar(request):
    url = request.GET.get("next", "/")
    parsed_uri = urlparse(url)
    if parsed_uri.netloc == '' or parsed_uri.netloc in DOMAINS_WHITELIST:
        return HttpResponseRedirect(url)
    return HttpResponseRedirect("/core")


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
