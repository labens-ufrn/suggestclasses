import os
import csv
import django
django.setup()
from dateutil.parser import parse
from dados.service.util import gravar_arquivo
from dados.service.funcoes_service import atualizar_funcao
from core.bo.docente import get_docente_by_siape
from core.models import Docente, FuncaoGratificada
from suggestclasses.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')

funcoes_atualizadas_list = list()


def main():
    os.chdir(DADOS_PATH)
    criar_funcoes_gratificadas()


def criar_funcoes_gratificadas():
    funcoes_gratificadas_csv = 'csv/funcoes-gratificadas.csv'
    print("\nCriando Funções Gratificadas: " + funcoes_gratificadas_csv + " para os Docentes do CERES ...!")

    with open(funcoes_gratificadas_csv) as csvfile:
        funcoes_gratificadas = csv.reader(csvfile, delimiter=';')
        next(funcoes_gratificadas)  # skip header

        for row in funcoes_gratificadas:
            carregar_funcoes_gratificadas(row)
        print()

    if funcoes_atualizadas_list:
        gravar_arquivo('funcoes_atualizados', funcoes_atualizadas_list)


def carregar_funcoes_gratificadas(row):
    siape = row[0] if row[0] != '' else None

    if Docente.objects.filter(siape=siape).exists():
        docente = get_docente_by_siape(siape)

        nome = row[1]
        situacao_servidor = row[2]
        id_unidade = row[3]
        lotacao = row[4]
        sigla = row[5]
        inicio = parse(row[6]) if row[6] != '' else None
        fim = parse(row[7]) if row[7] != '' else None
        id_unidade_designacao = row[8]
        unidade_designacao = row[9]
        atividade = row[10]
        observacoes = row[11]

        if not FuncaoGratificada.objects.filter(
           siape=siape, id_unidade=id_unidade, inicio=inicio, atividade=atividade).exists():
            print("Adicionando FuncaoGratificada " + siape + " - " + id_unidade + "- " + inicio.__str__() + " - " + atividade)
            fg = FuncaoGratificada(siape=siape, nome=nome, situacao_servidor=situacao_servidor,
                                   id_unidade=id_unidade, lotacao=lotacao, sigla=sigla,
                                   inicio=inicio, fim=fim, id_unidade_designacao=id_unidade_designacao,
                                   unidade_designacao=unidade_designacao, atividade=atividade,
                                   observacoes=observacoes)
            fg.save()
        else:
            funcao_antiga, atualizacoes = atualizar_funcao(
                siape, nome, situacao_servidor, id_unidade, lotacao, sigla, inicio, fim, 
                id_unidade_designacao, unidade_designacao, atividade, observacoes)
            if funcao_antiga and atualizacoes:
                funcoes_atualizadas_list.append(str(funcao_antiga) + ', ' + str(atualizacoes))
            else:
                print('.', end="")


if __name__ == "__main__":
    main()