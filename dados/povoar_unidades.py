import os
import csv
import django
django.setup()
from dateutil.parser import parse
from core.models import Centro, Departamento
from dados.service.util import gravar_arquivo
from dados.service.unidade_service import atualizar_unidade
from dados.service.util import gravar_arquivo
from suggestclasses.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')

unidades_atualizadas_list = list()


def main():
    os.chdir(DADOS_PATH)
    print("\nCriando Unidades do CERES e FELCS ...!")
    carregar_unidades()


def carregar_unidades():
    with open('csv/unidades.csv') as csvfile:
        unidades = csv.reader(csvfile, delimiter=';')
        next(unidades)  # skip header
        for row in unidades:
            carregar_unidade(row)
        print()

    if unidades_atualizadas_list:
        gravar_arquivo('unidades_atualizadas', unidades_atualizadas_list)


def carregar_unidade(row):
    id_dep = row[0]
    codigo_dep = row[1]
    nome_dep = row[2]
    new_nome_dep = add_acentos(nome_dep)
    sigla_dep = row[3]
    municipio = row[6]

    id_unidade_responsavel = row[9].strip()
    tipo_unidade_organizacional = row[17].strip()

    if (id_unidade_responsavel == '1482' or id_unidade_responsavel == '31011') and (tipo_unidade_organizacional == 'DEPARTAMENTO'
                                                or tipo_unidade_organizacional == 'ASSESSORIA'):
        if not Departamento.objects.filter(id_unidade=id_dep).exists():

            unidade_responsavel = Centro.objects.get(id_unidade=id_unidade_responsavel)

            d = Departamento(id_unidade=id_dep, codigo=codigo_dep, nome=new_nome_dep, sigla=sigla_dep,
                                endereco=municipio,
                                centro=unidade_responsavel)
            d.save()
        else:
            unidade_antiga, atualizacoes = atualizar_unidade(id_dep, codigo_dep, new_nome_dep, sigla_dep, municipio, id_unidade_responsavel)
            if unidade_antiga and atualizacoes:
                unidades_atualizadas_list.append(str(unidade_antiga) + ', ' + str(atualizacoes))
            else:
                print('.', end="")


def add_acentos(nome_dep: str) -> str:
    acentos = {
        'EDUCACAO': 'EDUCAÇÃO',
        'COMPUTACAO': 'COMPUTAÇÃO',
        'CIENCIAS': 'CIÊNCIAS',
        'CIENCIA': 'CIÊNCIA',
        'HISTORIA': 'HISTÓRIA',
        }

    nomes = nome_dep.split()
    for i, nome in enumerate(nomes):
        if nome in acentos:
            nomes[i] = acentos[nome]
    new_nome_dep = ' '.join(nomes)
    return new_nome_dep


if __name__ == "__main__":
    main()
