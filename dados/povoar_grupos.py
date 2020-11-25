import django
django.setup()
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Horario, SugestaoTurma, SolicitacaoTurma, VotoTurma


def main():
    print("Povoar Grupos e Permissões!")
    criar_grupos()


def criar_grupos():
    docentes, created = Group.objects.get_or_create(name='Docentes')
    adicionar_permissoes_docentes(docentes)

    discentes, created = Group.objects.get_or_create(name='Discentes')
    adicionar_permissoes_discentes(discentes)

    chefes, created = Group.objects.get_or_create(name='Chefes')
    adicionar_permissoes_chefes(chefes)

    coordenadores, created = Group.objects.get_or_create(name='Coordenadores')
    adicionar_permissoes_coordenadores(coordenadores)


def adicionar_permissoes_chefes(chefes):
    ct = ContentType.objects.get_for_model(SugestaoTurma)
    add_permissao(codename='view_sugestaoturma', content_type=ct, grupo=chefes)
    add_permissao(codename='change_sugestaoturma', content_type=ct, grupo=chefes)
    add_permissao(codename='add_sugestaoturma', content_type=ct, grupo=chefes)
    add_permissao(codename='delete_sugestaoturma', content_type=ct, grupo=chefes)

    ct = ContentType.objects.get_for_model(SolicitacaoTurma)
    add_permissao(codename='view_solicitacaoturma', content_type=ct, grupo=chefes)


def adicionar_permissoes_coordenadores(coordenadores):
    ct = ContentType.objects.get_for_model(SugestaoTurma)
    add_permissao(codename='view_sugestaoturma', content_type=ct, grupo=coordenadores)
    add_permissao(codename='change_sugestaoturma', content_type=ct, grupo=coordenadores)
    add_permissao(codename='add_sugestaoturma', content_type=ct, grupo=coordenadores)
    add_permissao(codename='delete_sugestaoturma', content_type=ct, grupo=coordenadores)

    ct = ContentType.objects.get_for_model(SolicitacaoTurma)
    add_permissao(codename='view_solicitacaoturma', content_type=ct, grupo=coordenadores)


def adicionar_permissoes_docentes(docentes):
    ct = ContentType.objects.get_for_model(SugestaoTurma)
    add_permissao(codename='view_sugestaoturma', content_type=ct, grupo=docentes)

    ct = ContentType.objects.get_for_model(SolicitacaoTurma)
    add_permissao(codename='view_solicitacaoturma', content_type=ct, grupo=docentes)


def adicionar_permissoes_discentes(discentes):
    ct = ContentType.objects.get_for_model(SugestaoTurma)
    add_permissao(codename='view_sugestaoturma', content_type=ct, grupo=discentes)

    ct = ContentType.objects.get_for_model(SolicitacaoTurma)
    add_permissao(codename='view_solicitacaoturma', content_type=ct, grupo=discentes)
    add_permissao(codename='add_solicitacaoturma', content_type=ct, grupo=discentes)
    add_permissao(codename='change_solicitacaoturma', content_type=ct, grupo=discentes)
    add_permissao(codename='delete_solicitacaoturma', content_type=ct, grupo=discentes)

    ct = ContentType.objects.get_for_model(VotoTurma)
    add_permissao(codename='view_vototurma', content_type=ct, grupo=discentes)
    add_permissao(codename='add_vototurma', content_type=ct, grupo=discentes)
    add_permissao(codename='change_vototurma', content_type=ct, grupo=discentes)
    add_permissao(codename='delete_vototurma', content_type=ct, grupo=discentes)


def add_permissao(codename, content_type, grupo):
    permission = Permission.objects.get(codename=codename, content_type=content_type)
    if permission not in grupo.permissions.all():
        grupo.permissions.add(permission)
        print('+', end="")
    else:
        print('.', end="")


if __name__ == "__main__":
    main()
