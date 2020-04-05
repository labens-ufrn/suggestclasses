import io
from random import sample
from typing import List
import logging
from urllib.parse import urlparse

import matplotlib.pyplot as plt
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views.generic import ListView, DetailView
from matplotlib.backends.backend_agg import FigureCanvasAgg

from core.models import Curso, ComponenteCurricular, EstruturaCurricular, OrganizacaoCurricular, \
    SugestaoTurma, Sala, Docente
from mysite.settings import DOMAINS_WHITELIST
from .bo.curso import get_cursos
from .bo.docente import get_docentes
from .bo.pedagogia import get_estrutura_pedagogia
from .bo.sala import get_salas
from .bo.sevices import get_oc_by_semestre, get_ch_by_semestre
from .bo.sistemas import get_estrutura_sistemas, get_estrutura_sistemas_dct
from .bo.turma import carrega_turmas, carrega_turmas_horario, \
    carrega_sugestao_turmas, atualiza_semestres
from .dao.centro_dao import get_ceres
from .dao.componente_dao import get_componentes_by_depto, get_componentes_curriculares
from .dao.departamento_dao import get_departamentos
from .forms import CadastroAlunoForm, SugestaoTurmaForm
from .models import Horario

# Get an instance of a logger
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

    context = {
        'ceres': ceres,
        'departamentos': departamentos,
        'docentes': docentes,
        'cursos': cursos,
        'componentes': componentes,
        'salas': salas,
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
    return render(request, 'core/flow/list.html')


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


def flow_bsi_op(request):
    id_ec = 510230607
    bsi_ec = EstruturaCurricular.objects.get(id_curriculo=id_ec)
    print(bsi_ec)
    bsi_oc_op = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=0)

    context = {
        'bsi_oc_op': bsi_oc_op,
    }

    return render(request, 'core/flow/bsi-op.html', context)


def flow_bsi_1b(request):
    bsi_ec = get_estrutura_sistemas_dct()

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

    return render(request, 'core/flow/bsi-1b.html', context)


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


def flow_ped_op(request):
    ped_ec = get_estrutura_pedagogia()
    ped_oc_op = get_oc_by_semestre(ped_ec, 0)

    context = {
        'ped_oc_op': ped_oc_op,
    }

    return render(request, 'core/flow/ped-op.html', context)


def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = CadastroAlunoForm(request.POST)
        if form_usuario.is_valid():
            usuario = form_usuario.save()
            grupo = form_usuario.cleaned_data.get('grupo')
            usuario.groups.add(grupo)
            username = form_usuario.cleaned_data.get('username')
            raw_password = form_usuario.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Usuário cadastrado com sucesso.')
            return redirect('index')
        else:
            messages.error(request, 'O formulário contém dados inválidos')
    else:
        form_usuario = CadastroAlunoForm()
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
    periodo = request.GET.getlist('periodo')

    turmas = carrega_turmas(bsi_dct, semestres, periodo)

    tt = carrega_turmas_horario(turmas)

    periodo_atual = [] if not periodo else periodo[0]
    semestres_atual = atualiza_semestres(semestres)

    context = {
        'tt': tt,
        'periodo_atual': periodo_atual,
        'semestres_atual': semestres_atual
    }

    return render(request, 'core/turma/bsi.html', context)


def turma_ped(request):
    ped_deduc = get_estrutura_pedagogia()

    semestres = request.GET.getlist('semestres')
    periodo = request.GET.getlist('periodo')

    turmas = carrega_turmas(ped_deduc, semestres, periodo)

    tt = carrega_turmas_horario(turmas)

    periodo_atual = [] if not periodo else periodo[0]
    semestres_atual = atualiza_semestres(semestres)

    context = {
        'tt': tt,
        'periodo_atual': periodo_atual,
        'semestres_atual': semestres_atual
    }

    return render(request, 'core/turma/ped.html', context)


def sugestao_list(request):
    return render(request, 'core/sugestao/list.html')


def sugestao_bsi_manter(request):
    """
            Lista todas as salas do centro.
    """
    bsi_dct = get_estrutura_sistemas_dct()
    semestres = ['100']
    semestres = atualiza_semestres(semestres)
    ano = 2020
    periodo = 1
    st_list = carrega_sugestao_turmas(bsi_dct, semestres, ano, periodo)

    context = {
        'sugestao_list': st_list
    }

    return render(request, 'core/sugestao/bsi/manter.html', context)


@permission_required("core.add_sugestao_turma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_bsi_incluir(request):
    if request.method == "POST":
        form_sugestao = SugestaoTurmaForm(request.POST)
        if form_sugestao.is_valid():
            sugestao_turma = form_sugestao.save(commit=False)
            sugestao_turma.tipo = 'REGULAR'
            sugestao_turma.campus_turma = sugestao_turma.local.campus
            sugestao_turma.save()
            messages.success(request, 'Sugestão de Turma cadastrada com sucesso.')
            return redirect('/core/sugestao/bsi/manter')
        else:
            messages.error(request, form_sugestao.errors['__all__'])
    else:
        form_sugestao = SugestaoTurmaForm()
    return render(request, 'core/sugestao/bsi/incluir.html', {'form_sugestao': form_sugestao})


def sugestao_bsi(request):
    bsi_dct = get_estrutura_sistemas_dct()

    semestres = request.GET.getlist('semestres')
    semestres = atualiza_semestres(semestres)

    turmas = carrega_sugestao_turmas(bsi_dct, semestres, ano=2020, periodo=1)

    tt = carrega_turmas_horario(turmas)

    context = {
        'tt': tt,
        'periodo_atual': '2020.1',
        'semestres_atual': semestres
    }

    return render(request, 'core/sugestao/bsi/list.html', context)


def sugestao_ped(request):
    ped_deduc = get_estrutura_pedagogia()

    semestres = request.GET.getlist('semestres')
    semestres = atualiza_semestres(semestres)

    turmas = carrega_sugestao_turmas(ped_deduc, semestres, ano=2020, periodo=1)

    tt = carrega_turmas_horario(turmas)

    context = {
        'tt': tt,
        'periodo_atual': '2020.1',
        'semestres_atual': semestres
    }

    return render(request, 'core/sugestao/ped/list.html', context)


@login_required(login_url='/core/usuario/logar')
def sugestao_ped_incluir(request):
    if request.method == "POST":
        form_sugestao = SugestaoTurmaForm(request.POST)
        if form_sugestao.is_valid():
            sugestao_turma = form_sugestao.save()
            sugestao_turma.save()
            messages.success(request, 'Sugestão de Turma cadastrada com sucesso.')
            return redirect('/core/sugestao/ped/list')
    else:
        form_sugestao = SugestaoTurmaForm()
    return render(request, 'core/sugestao/ped/incluir.html', {'form_sugestao': form_sugestao})


class SugestaoTurmaDetailView(DetailView):
    model = SugestaoTurma
    template_name = 'core/sugestao/bsi/sugestao_detail.html'


def create(request):
    if request.method == 'POST':
        sugestao_form = SugestaoTurmaForm(request.POST)
        if sugestao_form.is_valid():
            sugestao_form.save(commit=False)
            sugestao_form.tipo = 'REGULAR'
            sugestao_form.save()
            return redirect('sugestao_index')
    sugestao_form = SugestaoTurmaForm()

    return render(request, 'core/sugestao/bsi/create.html', {'form': sugestao_form})


@permission_required("core.change_sugestao_turma", login_url='/core/usuario/logar', raise_exception=True)
def edit(request, pk, template_name='core/sugestao/bsi/editar.html'):
    sugestao = get_object_or_404(SugestaoTurma, pk=pk)
    form = SugestaoTurmaForm(request.POST or None, instance=sugestao)
    if form.is_valid():
        form.save()
        messages.success(request, 'Sugestão de Turma alterada com sucesso.')
        return redirect('/core/sugestao/bsi/manter')
    else:
        messages.error(request, form.errors['__all__'])
    return render(request, template_name, {'form': form})


@permission_required("core.delete_sugestao_turma", login_url='/core/usuario/logar', raise_exception=True)
def delete(request, pk, template_name='core/sugestao/bsi/confirm_delete.html'):
    sugestao = get_object_or_404(SugestaoTurma, pk=pk)
    if request.method == 'POST':
        sugestao.delete()
        messages.success(request, 'Sugestão de Turma excluída com sucesso.')
        return redirect('/core/sugestao/bsi/manter')
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
