from datetime import datetime, date

from django.contrib import messages
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from core.models import Docente, FuncaoGratificada


def criar_usuario(request, form_usuario):
    usuario = form_usuario.save(commit=False)

    # check_username(request, form_usuario)
    check_email(request, form_usuario)
    grupos = check_grupos(request, form_usuario, usuario)

    usuario.save()
    for g in grupos:
        usuario.groups.add(g)


def check_username(request, form_usuario):
    username = form_usuario.cleaned_data.get('username')
    if User.objects.filter(username=username).exists():
        messages.error(request, 'O username informado já foi cadastrado!')
        raise ValidationError("O username já existe!")


def check_email(request, form_usuario):
    email = form_usuario.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
        msg = 'O e-mail informado já foi cadastrado!'
        messages.error(request, msg)
        form_usuario.add_error('email', msg)
        raise ValidationError("Email já existe!")


def check_grupos(request, form_usuario, usuario):
    matricula = form_usuario.cleaned_data.get('matricula')
    grupo_selecionado = form_usuario.cleaned_data.get('grupo')
    grupos = []
    if Docente.objects.filter(siape=matricula).exists():
        grupos.append(get_grupo_docentes())

        hoje = date.today()
        if FuncaoGratificada.objects.filter(siape=matricula, inicio__lte=hoje, fim__gt=hoje).exists():
            fgs = FuncaoGratificada.objects.filter(siape=matricula, inicio__lte=hoje, fim__gt=hoje)
            for fg in fgs:
                print(fg.atividade + " " + fg.atividade)
                if fg.atividade == 'CHEFE DE DEPARTAMENTO':
                    grupos.append(get_grupo_chefes())
                if fg.atividade == 'COORDENADOR DE CURSO':
                    grupos.append(get_grupo_coordenadores())
        return grupos
    # TODO Criar model de Discente para essa checagem
    # elif Discente.objects.filter(matricula=matricula).exists():
    #      grupo_chefes = form_usuario.cleaned_data.get('Chefes')
    #      usuario.groups.add(grupo_chefes)
    msg = 'A matrícula informada não está associada a um discente ou docente!'
    form_usuario.add_error('matricula', msg)
    messages.error(request, msg)
    raise ValidationError("A matrícula não foi encontrada!")


def get_grupo_docentes():
    docentes = 'Docentes'
    grupo_docentes = Group.objects.get(name=docentes)
    return grupo_docentes


def get_grupo_chefes():
    chefes = 'Chefes'
    grupo_chefes = Group.objects.get(name=chefes)
    return grupo_chefes


def get_grupo_coordenadores():
    coordenadores = 'Coordenadores'
    grupo_coordenadores = Group.objects.get(name=coordenadores)
    return grupo_coordenadores


def get_grupo_discentes():
    discentes = 'Discentes'
    grupo_discentes = Group.objects.get(name=discentes)
    return grupo_discentes


def autenticar_logar(request, form_usuario):
    username = form_usuario.cleaned_data.get('username')
    raw_password = form_usuario.cleaned_data.get('password1')
    user = authenticate(username=username, password=raw_password)
    login(request, user)
