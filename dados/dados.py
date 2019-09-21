import csv
import os
import django

django.setup()
from core.models import Curso, Centro, Departamento, ComponenteCurricular

DADOS_PATH = '/home/taciano/dev/workspace/suggestclasses/dados'


def main():
    print("Lendo dados sobre o CERES/UFRN ...!")
    os.chdir(DADOS_PATH)
    print(os.getcwd())

    # centros() # Não foi criado, adicionamos apenas o CERES.
    # departamentos()
    # cursos()
    componentes()


def departamentos():
    # Buscando o Centro CERES
    ceres = Centro.objects.get(id_unidade=1482)

    with open('unidades.csv') as csvfile:
        unidades = csv.reader(csvfile, delimiter=';')
        next(unidades)  # skip header

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
        next(cursos_ufrn)  # skip header

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


def componentes():
    print("Criando Componentes para os Departamentos do CERES ...!")

    with open('componentes-curriculares-presenciais.csv') as csvfile:
        componentes_ceres = csv.reader(csvfile, delimiter=';')
        next(componentes_ceres)  # skip header

        for row in componentes_ceres:

            unidade_responsavel = row[5].strip()

            if Departamento.objects.filter(nome=unidade_responsavel).exists():
                depto = Departamento.objects.get(nome=unidade_responsavel)
                print(depto)

                id_componente = row[0]
                tipo_componente = row[1]
                codigo_componente = row[2]
                nivel_componente = row[3]
                nome_componente = row[4]
                unidade_responsavel = row[5].strip()
                ch_teorico = row[6]
                ch_pratico = row[7]
                ch_estagio = row[8]
                ch_total = row[9]
                ch_dedicada_docente = row[10]
                ch_ead = row[11]
                cr_max_ead = row[12]
                equivalencia = row[16]
                pre_requisito = row[17]
                co_requisito = row[18]
                ementa = row[19]
                bibliografia = row[20]
                objetivos = row[21]
                conteudo = row[22]
                competencias_habilidades = row[23]
                referencias = row[24]
                ano_programa = row[25]
                periodo_programa = row[26]
                modalidade = row[27]
                curso_componente = row[28]

                if depto.id_unidade == 9726 or depto.id_unidade == 235:
                    print(id_componente)
                    print(tipo_componente)
                    print(codigo_componente)
                    print(nivel_componente)
                    print(nome_componente)
                    print(unidade_responsavel)
                    print(ch_teorico)
                    print(ch_pratico)
                    print(ch_estagio)
                    print(ch_total)
                    print(ch_dedicada_docente)
                    print(ch_ead)
                    print(cr_max_ead)
                    print(equivalencia)
                    print(pre_requisito)
                    print(co_requisito)
                    print(ementa)
                    #print(bibliografia)
                    #print(objetivos)
                    #print(conteudo)
                    #print(competencias_habilidades)
                    #print(referencias)
                    #print(ano_programa)
                    #print(periodo_programa)
                    print(modalidade)
                    print(curso_componente)

                    cc = ComponenteCurricular(id_componente=id_componente, tipo=tipo_componente,
                                              codigo=codigo_componente, nivel=nivel_componente, nome=nome_componente,
                                              ch_teorica=ch_teorico, ch_pratica=ch_pratico, ch_estagio=ch_estagio,
                                              ch_total=ch_total, ch_docente=ch_dedicada_docente, ch_ead=ch_ead,
                                              cr_max_ead=cr_max_ead, equivalencia=equivalencia,
                                              requisito=pre_requisito, corequisito=co_requisito, ementa=ementa,
                                              modalidade=modalidade, departamento=depto)
                    cc.save()


if __name__ == "__main__":
    main()
