import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from random import sample

from typing import List

from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect

from core.models import Curso, Departamento, ComponenteCurricular, Centro, EstruturaCurricular, OrganizacaoCurricular
from .bo.sevices import get_oc_by_semestre, get_ch_by_semestre
from .bo.pedagogia import get_estrutura_pedagogia
from .bo.sistemas import get_estrutura_sistemas_dct
from .bo.turma import get_turmas, get_turmas_por_horario
from .forms import CadastroAlunoForm
from .models import Horario
from django.db.models import Sum


def index(request):
    ceres = Centro.objects.get(id_unidade=1482)
    departamentos = Departamento.objects.all()
    estruturas = EstruturaCurricular.objects.all()
    dct = Departamento.objects.get(id_unidade=9726)
    print(dct)
    cursos = Curso.objects.all()
    componentes = ComponenteCurricular.objects.all()
    componentes_dct = ComponenteCurricular.objects.filter(departamento=dct)

    def get_componentes_by_depto(depto): return ComponenteCurricular.objects.filter(departamento=depto)

    componentes_by_depto = []
    headers: List[str] = []

    for d in departamentos:
        headers.append(d.sigla)
        componentes_by_depto.append(get_componentes_by_depto(d))

    template = loader.get_template('core/index.html')

    # response = requests.get("https://servicos.jfrn.jus.br/cartaapi/servicos")
    # comments = json.loads(response.content)

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


def list(request):
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
    departamentos = Departamento.objects.all()

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


def flow_list(request):
    return render(request, 'core/flow/list.html')


def flow_bsi(request):
    id_ec = 510230607
    bsi_ec = EstruturaCurricular.objects.get(id_curriculo=id_ec)

    def get_oc_by_semestre(semestre): return OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=semestre)

    get_ch_by_semestre = lambda ch: OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=s).aggregate(Sum(
        "componente__ch_total"))

    bsi_oc_semestres = []
    bsi_ch_semestres = []
    bsi_oc_op = get_oc_by_semestre(0)

    headers: List[str] = []

    for s in range(1, 9):
        headers.append(f"{s}º Semestre")
        bsi_oc_semestres.append(get_oc_by_semestre(s))
        bsi_ch_semestres.append(get_ch_by_semestre(s))

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


def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = CadastroAlunoForm(request.POST)
        if form_usuario.is_valid():
            usuario = form_usuario.save()
            grupo = Group.objects.get(name='Alunos')
            usuario.groups.add(grupo)
            username = form_usuario.cleaned_data.get('username')
            raw_password = form_usuario.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
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
            return redirect('index')
        else:
            form_login = AuthenticationForm()
    else:
        form_login = AuthenticationForm()
    return render(request, 'core/usuario/login.html', {'form_login': form_login})


@login_required(login_url='/core/usuario/logar')
def deslogar_usuario(request):
    logout(request)
    return redirect('index')


@login_required(login_url='/core/usuario/logar')
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('index')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'core/usuario/alterar_senha.html', {'form_senha': form_senha})


def turma_list(request):
    return render(request, 'core/turma/list.html')


def turma_bsi(request):
    horarios = []
    tt = []

    bsi_dct = get_estrutura_sistemas_dct()
    turmas1p = get_turmas(bsi_dct, 1)

    # Criar objeto para guardar Horário e Turmas;
    for i in range(1, 7):
        horario = Horario.objects.filter(ordem=i, turno='M').order_by('dia')
        horarios.append(horario)

    for i in range(1, 7):
        horario = Horario.objects.filter(ordem=i, turno='T').order_by('dia')
        horarios.append(horario)

    context = {
        'horarios': horarios,
        'turmas': turmas1p,
        'tt': tt
    }

    return render(request, 'core/turma/bsi.html', context)


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
