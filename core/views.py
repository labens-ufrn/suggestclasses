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
    print(bsi_ec)
    bsi_oc_1p = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=1)
    bsi_oc_2p = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=2)
    bsi_oc_3p = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=3)
    bsi_oc_4p = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=4)
    bsi_oc_5p = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=5)
    bsi_oc_6p = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=6)
    bsi_oc_7p = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=7)
    bsi_oc_8p = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=8)
    bsi_oc_op = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec, semestre=0)

    context = {
        'bsi_ec': bsi_ec,
        'bsi_oc_1p': bsi_oc_1p, 'bsi_oc_2p': bsi_oc_2p, 'bsi_oc_3p': bsi_oc_3p, 'bsi_oc_4p': bsi_oc_4p,
        'bsi_oc_5p': bsi_oc_5p, 'bsi_oc_6p': bsi_oc_6p, 'bsi_oc_7p': bsi_oc_7p, 'bsi_oc_8p': bsi_oc_8p,
        'bsi_oc_op': bsi_oc_op,
    }

    return render(request, 'core/flow/bsi.html', context)
