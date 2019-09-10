import csv
import os
import django

django.setup()
from core.models import Curso, Centro, Departamento

DADOS_PATH = '/home/taciano/dev/workspace/suggestclasses/dados'


def main():
    print("Lendo dados sobre o CERES/UFRN ...!")
    os.chdir(DADOS_PATH)
    print(os.getcwd())

    # centros() # Não foi criado, adicionamos apenas o CERES.
    departamentos()
    # cursos()


def departamentos():
    # Buscando o Centro CERES
    ceres = Centro.objects.get(id_unidade=1482)

    with open('unidades.csv') as csvfile:
        unidades = csv.reader(csvfile, delimiter=';')

        # dates = []
        # colors = []
        for row in unidades:

            id_dep = row[0]
            codigo_dep = row[1]
            nome_dep = row[2]
            sigla_dep = row[3]
            municipio = row[6]

            id_unidade_responsavel = row[9].strip()
            tipo_unidade_organizacional = row[17].strip()

            if id_unidade_responsavel == '1482' and (tipo_unidade_organizacional == 'DEPARTAMENTO'
                                                     or tipo_unidade_organizacional == 'ASSESSORIA'):
                print(id_dep)
                print(codigo_dep)
                print(nome_dep)
                print(sigla_dep)
                print(municipio)
                print(tipo_unidade_organizacional)
                print(id_unidade_responsavel)
                d = Departamento(id_unidade=id_dep, codigo=codigo_dep, nome=nome_dep, sigla=sigla_dep,
                                 endereco=municipio,
                                 centro=ceres)
                d.save()


def cursos():
    print("Criando cursos para o CERES ...!")
    # Buscando o Centro CERES
    ceres = Centro.objects.get(id_unidade=1482)

    with open('cursos-ufrn.csv') as csvfile:
        cursos_ufrn = csv.reader(csvfile, delimiter=';')

        # dates = []
        # colors = []
        for row in cursos_ufrn:

            id_curso = row[0]
            nome_curso = row[1]
            nivel_ensino = row[5]
            grau_academico = row[6]
            modalidade_educacao = row[7]
            turno = row[10]
            id_unidade_responsavel = row[14]

            if id_unidade_responsavel == '1482':
                print(id_curso)
                print(nome_curso)
                print(nivel_ensino)
                print(grau_academico)
                print(modalidade_educacao)
                print(turno)
                print(id_unidade_responsavel)
                c = Curso(codigo=id_curso, nome=nome_curso, nivel=nivel_ensino, grau=grau_academico,
                          modalidade=modalidade_educacao, turno=turno, centro=ceres)
                c.save()


if __name__ == "__main__":
    main()
