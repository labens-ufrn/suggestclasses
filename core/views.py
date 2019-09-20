from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json, requests

from core.models import Curso, Departamento
from .models import Horario


def index(request):
    cursos = Curso.objects.all()
    departamentos = Departamento.objects.all()

    template = loader.get_template('core/index.html')

    #response = requests.get("https://servicos.jfrn.jus.br/cartaapi/servicos")
    #comments = json.loads(response.content)

    context = {
        'departamentos': departamentos,
        'cursos': cursos
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
