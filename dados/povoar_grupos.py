import django
django.setup()
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Horario, SugestaoTurma


def main():
    print("Povoar Grupos e Permissões!")
    criar_grupos()


def criar_grupos():
    docentes, created = Group.objects.get_or_create(name='Docentes')

    discentes, created = Group.objects.get_or_create(name='Discentes')

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


def adicionar_permissoes_coordenadores(coordenadores):
    ct = ContentType.objects.get_for_model(SugestaoTurma)
    permission = Permission.objects.get(name="change_sugestaoturma")


def add_permissao(codename, content_type, grupo):
    permission = Permission.objects.get(codename=codename, content_type=content_type)
    if permission not in grupo.permissions.all():
        grupo.permissions.add(permission)
        print('+', end="")
    else:
        print('.', end="")


if __name__ == "__main__":
    main()
