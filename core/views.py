from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json, requests

from core.models import Curso, Departamento, ComponenteCurricular, Centro, EstruturaCurricular, OrganizacaoCurricular
from .models import Horario


def index(request):
    ceres = Centro.objects.get(id_unidade=1482)
    departamentos = Departamento.objects.all()
    estruturas = EstruturaCurricular.objects.all()
    dct = Departamento.objects.get(id_unidade=9726)
    print(dct)
    cursos = Curso.objects.all()
    componentes = ComponenteCurricular.objects.filter(departamento=dct)
    print(componentes)

    template = loader.get_template('core/index.html')

    # response = requests.get("https://servicos.jfrn.jus.br/cartaapi/servicos")
    # comments = json.loads(response.content)

    context = {
        'ceres': ceres,
        'departamentos': departamentos,
        'cursos': cursos,
        'componentes': componentes,
        'estruturas': estruturas
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

    get_oc_by_semestre = lambda s: OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=s)

    bsi_ocs_semestre = []
    oc_bsi = get_oc_by_semestre(0)

    headers: List[str] = []

    for i in range(1, 9):
        headers.append(f"{i}º Semestre")
        bsi_ocs_semestre.append(get_oc_by_semestre(i))

    context = {
        'bsi_ec': bsi_ec,
        'headers': headers,
        'bsi_ocs_semestre': bsi_ocs_semestre,
        'oc_bsi': oc_bsi,
    }

    return render(request, 'core/flow/bsi.html', context)
