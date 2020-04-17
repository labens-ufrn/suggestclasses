from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

from core.models import Docente, FuncaoGratificada, Discente


def criar_usuario(request, form_usuario):
    usuario = form_usuario.save(commit=False)

    # check_username(request, form_usuario)
    check_email(request, form_usuario)
    grupos = check_grupos(request, form_usuario, usuario)

    usuario.save()
    for g in grupos:
        check_usuario(usuario, form_usuario, g)
        usuario.groups.add(g)
    return usuario


def check_usuario(usuario, form_usuario, g):
    matricula = form_usuario.cleaned_data.get('matricula')
    if g.name == 'Docentes' and Docente.objects.filter(siape=matricula).exists():
        docente = Docente.objects.get(siape=matricula)
        docente.usuario = usuario
        docente.save()
    elif g.name == 'Discentes' and Discente.objects.filter(matricula=matricula).exists():
        discente = Discente.objects.get(matricula=matricula)
        discente.usuario = usuario
        discente.save()


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
    grupos = []
    if Docente.objects.filter(siape=matricula).exists():
        grupos.append(get_grupo_docentes())
        check_gestor(grupos, matricula)
        return grupos
    # Realiza a checagem da existência do aluno e verifica se têm matrícula ativa
    elif Discente.objects.filter(matricula=matricula).exists():
        check_discente_ativo(form_usuario, grupos, matricula)
        return grupos
    # TODO Acrescentar checagem para Servidores do Apoio e Secretários de Curso/Departamento

    msg = 'A matrícula informada não está associada a um discente ou docente do CERES!'
    form_usuario.add_error('matricula', msg)
    messages.error(request, msg)
    raise ValidationError("A matrícula não foi encontrada no CERES!")


def check_discente_ativo(form_usuario, grupos, matricula):
    discente = Discente.objects.get(matricula=matricula)
    if discente.status == 'ATIVO' or discente.status == 'ATIVO - FORMANDO':
        grupos.append(get_grupo_discentes())
    else:
        msg = 'A matrícula do discente informada não está ATIVA!'
        form_usuario.add_error('matricula', msg)


def check_gestor(grupos, matricula):
    hoje = date.today()
    if FuncaoGratificada.objects.filter(siape=matricula, inicio__lte=hoje, fim__gt=hoje).exists():
        fgs = FuncaoGratificada.objects.filter(siape=matricula, inicio__lte=hoje, fim__gt=hoje)
        for fg in fgs:
            if fg.atividade == 'CHEFE DE DEPARTAMENTO':
                grupos.append(get_grupo_chefes())
            if fg.atividade == 'COORDENADOR DE CURSO':
                grupos.append(get_grupo_coordenadores())


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
