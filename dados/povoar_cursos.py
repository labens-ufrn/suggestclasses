import os
import csv
import django
django.setup()
from core.models import Centro, Curso
from core.bo.docente import get_docente_by_nome
from dados.service.curso_service import atualizar_curso
from dados.service.util import gravar_arquivo
from suggestclasses.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')

cursos_atualizados_list = list()


def main():
    os.chdir(DADOS_PATH)
    print("\nCriando Cursos do CERES ...!")
    carregar_cursos()


def carregar_cursos():
    with open('csv/cursos-ufrn.csv') as csvfile:
        cursos_ufrn = csv.reader(csvfile, delimiter=';')
        next(cursos_ufrn)  # skip header

        for row in cursos_ufrn:
            carregar_curso(row)
        print()

    if cursos_atualizados_list:
        gravar_arquivo('cursos_atualizados', cursos_atualizados_list)

def carregar_curso(row):
    id_curso = row[0]
    nome_curso = row[1]
    coordenador = row[3]
    nivel_ensino = row[5]
    grau_academico = row[6]
    modalidade_educacao = row[7]
    turno = row[10]
    id_unidade_responsavel = row[14]

    if id_unidade_responsavel == '1482':
        # Buscando o Centro CERES
        ceres = Centro.objects.get(id_unidade=1482)
        # TODO a busca foi feita pelo nome pois na tabela curso não tem o SIAPE do coordenador
        docente = get_docente_by_nome(coordenador)
        if not Curso.objects.filter(codigo=id_curso).exists():
            c = Curso(codigo=id_curso, nome=nome_curso, coordenador=docente, nivel=nivel_ensino,
                        grau=grau_academico, modalidade=modalidade_educacao, turno=turno, centro=ceres)
            c.save()
            print('+', end="")
        else:
            curso_antigo, atualizacoes = atualizar_curso(id_curso, nome_curso, docente, nivel_ensino, \
                grau_academico, modalidade_educacao, turno, ceres)
            if curso_antigo and atualizacoes:
                cursos_atualizados_list.append(str(curso_antigo) + ', ' + str(atualizacoes))
            else:
                print('.', end="")

if __name__ == "__main__":
    main()
