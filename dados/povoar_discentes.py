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
    # carregar_discentes_anual('csv/discentes-2021.csv')


def carregar_discentes_anual(discentes_csv):
    print("\nCriando Discentes Ingressantes: " + discentes_csv + " para os Cursos do CERES ...!")

    with open(discentes_csv) as csvfile:
        discentes = csv.reader(csvfile, delimiter=';')
        next(discentes)  # skip header

        for row in discentes:
            carregar_discente(row)
        print()

    if discentes_atualizados_list:
        gravar_arquivo(discentes_csv[4:-4] + "_atualizados ", discentes_atualizados_list)


def carregar_discente(row):
    id_unidade = row[13] if row[13] != '' else None
    # id_unidade = row[4] if row[4] != '' else None
    # Carregamento apenas de alunos do CERES.
    if Centro.objects.filter(id_unidade=id_unidade).exists():
        matricula = row[0]
        nome_discente = row[1]
        # nome_discente = row[6]
        sexo = row[2]
        # sexo = row[7]
        ano_ingresso = row[3]
        # ano_ingresso = row[1]
        periodo_ingresso = row[4]
        # periodo_ingresso = row[2]
        forma_ingresso = row[5]
        # forma_ingresso = row[8]
        tipo_discente = row[6]
        # tipo_discente = row[9]
        status = row[7]
        # status = row[10]
        sigla_nivel_ensino = row[8]
        # sigla_nivel_ensino = row[11]
        nivel_ensino = row[9]
        # nivel_ensino = row[12]
        id_curso = row[10]
        # id_curso = row[3]
        nome_curso = row[11]
        # nome_curso = row[13]
        modalidade_educacao = row[12]
        # modalidade_educacao = row[14]
        # id_unidade = row[13]
        nome_unidade = row[14]
        # nome_unidade = row[15]
        id_unidade_gestora = row[15]
        # id_unidade_gestora = row[5]
        nome_unidade_gestora = row[16]
        # nome_unidade_gestora = row[16]

        if not Discente.objects.filter(matricula=matricula).exists():
            print("Adicionando Discente " + matricula + " - " + nome_discente + "- " + nome_curso)
            if sexo == "M" or sexo == "F":
                sexo = sexo
            else:
                sexo = ""
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
