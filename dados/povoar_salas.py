import os
import csv
import django
django.setup()
from suggestclasses.settings import BASE_DIR
from core.models import Sala, Centro
DADOS_PATH = os.path.join(BASE_DIR, 'dados')


def main():
    os.chdir(DADOS_PATH)
    carregar_salas()


def carregar_salas():
    print("\nCriando Salas para o CERES ...!")

    with open('csv/salas-ceres.csv') as csvfile:
        salas = csv.reader(csvfile, delimiter=',')
        next(salas)  # skip header

        for row in salas:
            carregar_sala(row)
        print()


def carregar_sala(row):
    nome = row[0]
    sigla = row[1]
    capacidade = row[2]
    tamanho = row[3] if row[3] != '0.0' else None
    bloco = row[4]
    centro_id = row[5]
    campus_id = row[6]

    ceres = Centro.objects.get(pk=centro_id)
    # campus = Sala.CAMPUS_CHOICES[campus_id-1]
    ss = Sala.objects.filter(nome=nome, sigla=sigla, bloco=bloco,
                             centro=ceres, campus=campus_id)
    if not Sala.objects.filter(nome=nome, sigla=sigla,
                               tamanho=tamanho, bloco=bloco,
                               centro=ceres, campus=campus_id).exists():
        Sala.objects.create(nome=nome, sigla=sigla, capacidade=capacidade,
                            tamanho=tamanho, bloco=bloco,
                            centro=ceres, campus=campus_id)
        print('+', end="")
    else:
        print('.', end="")


if __name__ == "__main__":
    main()
