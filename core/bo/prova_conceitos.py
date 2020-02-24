import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from core.bo.sistemas import get_estrutura_sistemas, criar_organizacao_sistemas_dct, get_estrutura_sistemas_dct
from core.bo.turma import get_turmas


def main():
    print("Executável para testes de conceitos e ideias!")
    print(os.getcwd())

    # criar_organizacao_sistemas_dct()

    bsi_dct = get_estrutura_sistemas_dct()

    turmas1p = get_turmas(bsi_dct, 1)

    for t in turmas1p:
        print('Turma: ' + t.__str__())
        print(t)

    get_turmas(bsi_dct, 2)


if __name__ == "__main__":
    main()
