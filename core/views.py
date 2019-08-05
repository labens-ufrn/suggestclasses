from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import Horario

def index(request):
    horario_list = Horario.objects.all()
    template = loader.get_template('core/index.html')
    context = {
        'horario_list': horario_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, horario_id):
    return HttpResponse("You're looking at Horario %s." % horario_id)

def list(request):
    horario_list = Horario.objects.all()
    context = {'horario_list': horario_list}
    return render(request, 'core/list.html', context)
