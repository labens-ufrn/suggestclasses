import os
import csv
import django
django.setup()
from datetime import datetime
from dateutil.parser import parse
from core.models import Departamento, Docente
from dados.service.docente_service import atualizar_docente
from suggestclasses.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')

docentes_atualizados_set = list()


def main():
    os.chdir(DADOS_PATH)
    carregar_docentes()


def carregar_docentes():
    print("\nCriando Docentes do CERES ...!")

    with open('docentes.csv') as csvfile:
        docentes = csv.reader(csvfile, delimiter=';')
        next(docentes)  # skip header

        for row in docentes:
            carregar_docente(row)
        print()
    
    data_e_hora_atuais = datetime.now()
    docentes_atualizados = open("docentes_atualizados " + str(data_e_hora_atuais) + ".txt", "a")
    for docente_modificados in docentes_atualizados_set:
    # \n is placed to indicate EOL (End of Line)
        docentes_atualizados.write(docente_modificados + '\n')
    docentes_atualizados.close()


def carregar_docente(row):
    siape = row[0]
    nome = row[1]
    sexo = row[2]
    formacao = row[3]
    tipo_jornada_trabalho = row[4]
    vinculo = row[5]
    categoria = row[6]
    classe_funcional = row[7]
    id_unidade_lotacao = row[8]
    lotacao = row[9]
    admissao_str = row[10]
    # https://stackabuse.com/converting-strings-to-datetime-in-python/
    admissao = parse(admissao_str)

    if id_unidade_lotacao == '1482' or Departamento.objects.filter(id_unidade=id_unidade_lotacao).exists():

        depto = None
        if Departamento.objects.filter(id_unidade=id_unidade_lotacao).exists():
            depto = Departamento.objects.get(id_unidade=id_unidade_lotacao)
        else:
            print('Docente não vinculado a Departamento: ')
            print(str(siape) + ' - ' + nome + ' - ' + lotacao)

        if not Docente.objects.filter(siape=siape).exists():
            print("Adicionando Docente: " + siape + " - " + nome)
            professor = Docente(siape=siape, nome=nome, sexo=sexo, formacao=formacao,
                                tipo_jornada_trabalho=tipo_jornada_trabalho,
                                vinculo=vinculo, categoria=categoria, classe_funcional=classe_funcional,
                                id_unidade_lotacao=id_unidade_lotacao, lotacao=lotacao, admissao=admissao,
                                departamento=depto)
            professor.save()
            print('+', end="")
        else:
            docente = Docente.objects.get(siape=siape)
            if docente.departamento is None:
                docente.departamento = depto
                docente.save()
            
            docente_antigo, atualizacoes = atualizar_docente(
                siape, nome, sexo, formacao, tipo_jornada_trabalho, vinculo, categoria, \
                classe_funcional, id_unidade_lotacao, lotacao, admissao, depto)
            if docente_antigo and atualizacoes:
                docentes_atualizados_set.append(str(docente_antigo) + ', ' + str(atualizacoes))
            else:
                print('.', end="")


if __name__ == "__main__":
    main()
