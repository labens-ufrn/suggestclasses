import csv
from dados.povoar_unidades import carregar_unidades
import os
import django
django.setup()
from dados.povoar_organizacao_curricular import adicionar_componentes_pedagogia, criar_estrutura_sistemas_dct, criar_organizacao_sistemas_dct
from dados.povoar_estruturas import carregar_estruturas
from dados.povoar_grupos import adicionar_grupos
from dados.povoar_horarios import povoar_horarios
from suggestclasses.settings import BASE_DIR
from dados.baixar_dados import downloads_dados
from dados.povoar_componentes import carregar_componentes
from dados.povoar_docentes import carregar_docentes
from dados.povoar_cursos import carregar_cursos
from dados.povoar_funcoes_gratificadas import carregar_funcoes_gratificadas
from dados.povoar_turma import carregar_turmas
from dados.povoar_discentes import carregar_discentes
from dados.povoar_salas import carregar_sala
from core.models import Curso, Centro, Departamento, ComponenteCurricular, EstruturaCurricular, \
    OrganizacaoCurricular
from core.bo.docente import get_docente_by_nome
from datetime import datetime

DADOS_PATH = os.path.join(BASE_DIR, 'dados')


def main():
    print("Lendo dados sobre o CERES/UFRN ...!")
    print(os.getcwd())
    print(os.path.join(BASE_DIR, 'dados'))
    os.chdir(DADOS_PATH)
    print(os.getcwd())
    print(os.path.join(BASE_DIR, 'dados'))

    downloads_dados()
    criar_horarios()
    criar_grupos()
    centros()  # Adicionamos apenas o CERES.
    criar_salas()
    departamentos()
    criar_docentes()
    criar_cursos()
    criar_componentes()
    estruturas()
    organizacao()
    criar_turmas()
    criar_funcoes_gratificadas()
    criar_discentes()


def criar_horarios():
    print("Povoar Horários da UFRN!")
    povoar_horarios()
    print()


def criar_grupos():
    print("Povoar Grupos e Permissões!")
    adicionar_grupos()
    print()


def centros():
    print("\nCriando centros CERES e FELCS...!")
    ceres = Centro(id_unidade=1482, codigo=1800, nome='Centro de Ensino Superior do Seridó',
                    sigla='CERES', endereco='Rua Joaquim Gregório, Penedo, Caicó - RN',
                    site='https://www.ceres.ufrn.br/')
    felcs = Centro(id_unidade=31011, codigo=1170, nome='FACULDADE DE ENGENHARIA, LETRAS E CIENCIAS SOCIAIS DO SERIDO',
                    sigla='FELCS', endereco='Currais Novos - RN',
                    site='https://www.ceres.ufrn.br/')
    if not Centro.objects.filter(id_unidade=1482).exists():
        ceres.save()
    if not Centro.objects.filter(id_unidade=31011).exists():
        felcs.save()
    else:
        print('.', end="")


def criar_salas():
    # Buscando o Centro CERES
    print("\nCriando Salas para o CERES ...!")

    with open('csv/salas-ceres.csv') as csvfile:
        salas = csv.reader(csvfile, delimiter=',')
        next(salas)  # skip header

        for row in salas:
            carregar_sala(row)
        print()


def departamentos():
    # Buscando o Centro CERES
    print("\nCriando Departamentos para o CERES ...!")
    carregar_unidades()


def criar_docentes():
    print("\nCriando Docentes do CERES ...!")
    carregar_docentes()


def criar_cursos():
    print("\nCriando cursos para o CERES ...!")
    carregar_cursos()


def criar_componentes():
    print("\nCriando Componentes para os Departamentos do CERES ...!")
    carregar_componentes()


def estruturas():
    print("\nCriando Estruturas Curriculares para os Cursos do CERES ...!")
    carregar_estruturas()


def organizacao():
    print("\nCriando Organizações Curriculares para os Cursos do CERES ...!")

    with open('csv/curriculo-componente-graduacao.csv') as csvfile:
        ccg = csv.reader(csvfile, delimiter=';')
        next(ccg)  # skip header

        for row in ccg:

            id_estrutura = row[1]
            id_componente_curricular = row[2]

            if EstruturaCurricular.objects.filter(id_curriculo=id_estrutura).exists():
                ec = EstruturaCurricular.objects.get(id_curriculo=id_estrutura)

                if ComponenteCurricular.objects.filter(id_componente=id_componente_curricular).exists():
                    cc = ComponenteCurricular.objects.get(id_componente=id_componente_curricular)

                    id_curriculo_comp = row[0]

                    semestre_oferta = row[3]
                    tipo_vinculo_componente = row[4]
                    nivel_ensino = row[5]

                    if not OrganizacaoCurricular.objects.filter(id_curriculo_componente=id_curriculo_comp).exists():
                        print("Adicionando Docente: " + id_curriculo_comp + " - " + ec.curso.nome + " - " +
                              cc.codigo + " - " + cc.nome)
                        oc = OrganizacaoCurricular(id_curriculo_componente=id_curriculo_comp, estrutura=ec,
                                                   componente=cc, semestre=semestre_oferta,
                                                   tipo_vinculo=tipo_vinculo_componente, nivel=nivel_ensino)
                        oc.save()
                    else:
                        print('.', end="")
        print()
    print("Criando Organizações Modificadas - SuggestClasses ...!")
    adicionar_componentes_pedagogia()
    criar_estrutura_sistemas_dct()
    criar_organizacao_sistemas_dct()


def criar_turmas():
    print("\nCriando Turmas 2019.1, 2019.2 e 2020.1 para os Cursos do CERES ...!")
    carregar_turmas()


def criar_funcoes_gratificadas():
    funcoes_gratificadas_csv = 'csv/funcoes-gratificadas.csv'
    print("\nCriando Funções Gratificadas: " + funcoes_gratificadas_csv + " para os Docentes do CERES ...!")

    with open(funcoes_gratificadas_csv) as csvfile:
        funcoes_gratificadas = csv.reader(csvfile, delimiter=';')
        next(funcoes_gratificadas)  # skip header

        for row in funcoes_gratificadas:
            carregar_funcoes_gratificadas(row)
        print()


def criar_discentes():
    print("\nCriando Discentes por Ano de Ingresso para os Cursos do CERES ...!")
    carregar_discentes()


if __name__ == "__main__":
    main()
