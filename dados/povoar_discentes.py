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
    criar_discentes()


def criar_discentes():
    print("\nCriando Discentes por Ano de Ingresso para os Cursos do CERES ...!")

    criar_discentes_anual('discentes-2009.csv')
    criar_discentes_anual('discentes-2010.csv')
    criar_discentes_anual('discentes-2011.csv')
    criar_discentes_anual('discentes-2012.csv')
    criar_discentes_anual('discentes-2013.csv')
    criar_discentes_anual('discentes-2014.csv')
    criar_discentes_anual('discentes-2015.csv')
    criar_discentes_anual('discentes-2016.csv')
    criar_discentes_anual('discentes-2017.csv')
    criar_discentes_anual('discentes-2018.csv')
    criar_discentes_anual('discentes-2019.csv')
    criar_discentes_anual('discentes-2020.csv')


def criar_discentes_anual(discentes_csv):
    print("\nCriando Discentes Ingressantes: " + discentes_csv + " para os Cursos do CERES ...!")

    with open(discentes_csv) as csvfile:
        discentes = csv.reader(csvfile, delimiter=';')
        next(discentes)  # skip header

        for row in discentes:
            carregar_discentes(row)
        print()

    data_e_hora_atuais = datetime.now()
    discentes_atualizados = open("atualizados/" + discentes_csv[:-4] + "_atualizados " + str(data_e_hora_atuais) + ".txt", "a")
    for discente_modificados in discentes_atualizados_list:
    # \n is placed to indicate EOL (End of Line)
        discentes_atualizados.write(discente_modificados + '\n')
    discentes_atualizados.close()

def carregar_discentes(row):
    id_unidade = row[13] if row[13] != '' else None

    # Carregamento apenas de alunos do CERES.
    if Centro.objects.filter(id_unidade=id_unidade).exists():
        matricula = row[0]
        nome_discente = row[1]
        sexo = row[2]
        ano_ingresso = row[3]
        periodo_ingresso = row[4]
        forma_ingresso = row[5]
        tipo_discente = row[6]
        status = row[7]
        sigla_nivel_ensino = row[8]
        nivel_ensino = row[9]
        id_curso = row[10]
        nome_curso = row[11]
        modalidade_educacao = row[12]
        id_unidade = row[13]
        nome_unidade = row[14]
        id_unidade_gestora = row[15]
        nome_unidade_gestora = row[16]

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
                discente_atualizados_list.add(str(discente_antigo) + ', ' + str(atualizacoes))
            else:
                print('.', end="")

if __name__ == "__main__":
    main()