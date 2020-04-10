from django.contrib import messages
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from core.models import Docente

grupos = []


def criar_usuario(request, form_usuario):
    usuario = form_usuario.save(commit=False)

    # check_username(request, form_usuario)
    check_email(request, form_usuario)
    check_grupos(request, form_usuario, usuario)

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

    if Docente.objects.filter(siape=matricula).exists():
        docentes = 'Docentes'
        if Group.objects.filter(name=docentes).exists():
            grupo_docentes = Group.objects.get(name=docentes)
            grupos.append(grupo_docentes)
            return
        # TODO Criar model de Função Gratificada para essa checagem
        # if FuncaoGratificada.objects.filter(siape=matricula).exists():
        #    grupo_chefes = form_usuario.cleaned_data.get('Chefes')
        #    usuario.groups.add(grupo_chefes)
    # TODO Criar model de Discente para essa checagem
    # elif Discente.objects.filter(matricula=matricula).exists():
    #      grupo_chefes = form_usuario.cleaned_data.get('Chefes')
    #      usuario.groups.add(grupo_chefes)

    messages.error(request, 'A matrícula informada não está associada a um discente ou docente!')
    raise ValidationError("A matrícula não foi encontrada!")


def autenticar_logar(request, form_usuario):
    username = form_usuario.cleaned_data.get('username')
    raw_password = form_usuario.cleaned_data.get('password1')
    user = authenticate(username=username, password=raw_password)
    login(request, user)
