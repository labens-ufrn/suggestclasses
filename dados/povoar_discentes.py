from dados.service.util import gravar_arquivo
from datetime import datetime
import os
import csv
import django
django.setup()
from dados.service.discente_service import atualizar_discente
from core.models import Centro, Discente
from suggestclasses.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')

discentes_atualizados_list =list()


def main():
    os.chdir(DADOS_PATH)
    print("\nCriando Discentes por Ano de Ingresso para os Cursos do CERES ...!")
    carregar_discentes()


def carregar_discentes():
    carregar_discentes_anual('csv/discentes-2009.csv')
    carregar_discentes_anual('csv/discentes-2010.csv')
    carregar_discentes_anual('csv/discentes-2011.csv')
    carregar_discentes_anual('csv/discentes-2012.csv')
    carregar_discentes_anual('csv/discentes-2013.csv')
    carregar_discentes_anual('csv/discentes-2014.csv')
    carregar_discentes_anual('csv/discentes-2015.csv')
    carregar_discentes_anual('csv/discentes-2016.csv')
    carregar_discentes_anual('csv/discentes-2017.csv')
    carregar_discentes_anual('csv/discentes-2018.csv')
    carregar_discentes_anual('csv/discentes-2019.csv')
    carregar_discentes_anual('csv/discentes-2020.csv')
    carregar_discentes_anual('csv/discentes-2021.csv')
    carregar_discentes_anual('csv/discentes-2022.csv')
    carregar_discentes_anual('csv/discentes-2023.csv')
    carregar_discentes_anual('csv/discentes-2024.csv')

## Utilizamos a leitura do csv usando os headers
## Página: https://docs.python.org/pt-br/3/library/csv.html
def carregar_discentes_anual(discentes_csv):
    print("\nCriando Discentes Ingressantes: " + discentes_csv + " para os Cursos do CERES ...!")

    with open(discentes_csv) as csvfile:
        discentes = csv.DictReader(csvfile, delimiter=';')

        for row in discentes:
            carregar_discente(row)
        print()

    if discentes_atualizados_list:
        gravar_arquivo(discentes_csv[4:-4] + "_atualizados ", discentes_atualizados_list)


def carregar_discente(row):
    id_unidade = row['id_unidade'] if row['id_unidade'] != '' else None
    # Carregamento apenas de alunos do CERES e FELCS.
    if Centro.objects.filter(id_unidade=id_unidade).exists():
        matricula = row['matricula']
        nome_discente = row['nome_discente']
        sexo = row['sexo']
        ano_ingresso = row['ano_ingresso']
        periodo_ingresso = row['periodo_ingresso']
        forma_ingresso = row['forma_ingresso']
        tipo_discente = row['tipo_discente']
        status = row['status']
        sigla_nivel_ensino = row['sigla_nivel_ensino']
        nivel_ensino = row['nivel_ensino']
        id_curso = row['id_curso']
        nome_curso = row['nome_curso']
        modalidade_educacao = row['modalidade_educacao']
        nome_unidade = row['nome_unidade']
        id_unidade_gestora = row['id_unidade_gestora']
        nome_unidade_gestora = row['nome_unidade_gestora']

        if not Discente.objects.filter(matricula=matricula).exists():
            print("Adicionando Discente " + matricula + " - " + nome_discente + "- " + nome_curso)
            if sexo == 'false':
                sexo = 'F'
            if sexo != 'M' and sexo != 'F':
                sexo = ''
            discente = Discente(matricula=matricula, nome_discente=nome_discente, sexo=sexo,
                                ano_ingresso=ano_ingresso, periodo_ingresso=periodo_ingresso,
                                forma_ingresso=forma_ingresso, tipo_discente=tipo_discente, status=status,
                                sigla_nivel_ensino=sigla_nivel_ensino, nivel_ensino=nivel_ensino,
                                id_curso=id_curso, nome_curso=nome_curso, modalidade_educacao=modalidade_educacao,
                                id_unidade=id_unidade, nome_unidade=nome_unidade,
                                id_unidade_gestora=id_unidade_gestora, nome_unidade_gestora=nome_unidade_gestora)
            discente.save()
        else:
            discente_antigo, atualizacoes = atualizar_discente(
                matricula, nome_discente, sexo, ano_ingresso, periodo_ingresso, forma_ingresso,
                tipo_discente, status, sigla_nivel_ensino, nivel_ensino, id_curso, nome_curso,
                modalidade_educacao, id_unidade, nome_unidade, id_unidade_gestora, nome_unidade_gestora)
            if discente_antigo and atualizacoes:
                discentes_atualizados_list.append(str(discente_antigo) + ', ' + str(atualizacoes))
            else:
                print('.', end="")


if __name__ == "__main__":
    main()
