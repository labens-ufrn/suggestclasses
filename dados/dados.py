import csv
import os
import django

django.setup()
from core.models import Curso, Centro, Departamento, ComponenteCurricular, EstruturaCurricular, OrganizacaoCurricular

DADOS_PATH = '/home/taciano/dev/workspace/suggestclasses/dados'


def main():
    print("Lendo dados sobre o CERES/UFRN ...!")
    os.chdir(DADOS_PATH)
    print(os.getcwd())

    # centros() # Não foi criado, adicionamos apenas o CERES.
    # departamentos()
    # cursos()
    componentes()
    # estruturas()
    organizacao()


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
                print("Departamento " + depto.sigla)

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

                # if depto.id_unidade == 9726 or depto.id_unidade == 235:
                print(id_componente)

                cc = ComponenteCurricular(id_componente=id_componente, tipo=tipo_componente,
                                          codigo=codigo_componente, nivel=nivel_componente, nome=nome_componente,
                                          ch_teorica=ch_teorico, ch_pratica=ch_pratico, ch_estagio=ch_estagio,
                                          ch_total=ch_total, ch_docente=ch_dedicada_docente, ch_ead=ch_ead,
                                          cr_max_ead=cr_max_ead, equivalencia=equivalencia,
                                          requisito=pre_requisito, corequisito=co_requisito, ementa=ementa,
                                          modalidade=modalidade, departamento=depto)
                cc.save()


def estruturas():
    print("Criando Estruturas Curriculares para os Cursos do CERES ...!")

    with open('estruturas-curriculares.csv') as csvfile:
        estruturas_ceres = csv.reader(csvfile, delimiter=';')
        next(estruturas_ceres)  # skip header

        for row in estruturas_ceres:

            curso_ufrn = row[3]

            if Curso.objects.filter(codigo=curso_ufrn).exists():
                curso_ceres = Curso.objects.get(codigo=curso_ufrn)
                print(curso_ceres)

                id_curriculo = row[0]
                codigo = row[1]
                nome_matriz = row[2]
                id_curso = row[3]
                nome_curso = row[4]
                semestre_conclusao_minimo = row[5] if row[5] != '' else None
                semestre_conclusao_ideal = row[6] if row[6] != '' else None
                semestre_conclusao_maximo = row[7] if row[7] != '' else None
                meses_conclusao_minimo = row[8] if row[8] != '' else None
                meses_conclusao_ideal = row[9] if row[9] != '' else None
                meses_conclusao_maximo = row[10] if row[10] != '' else None
                cr_total_minimo = row[11] if row[11] != '' else None
                ch_total_minima = row[12] if row[12] != '' else None
                ch_optativas_minima = row[13] if row[13] != '' else None
                ch_complementar_minima = row[14] if row[14] != '' else None
                max_eletivos = row[15] if row[15] != '' else None
                ch_nao_atividade_obrigatoria = row[16] if row[16] != '' else None
                cr_nao_atividade_obrigatorio = row[17] if row[17] != '' else None
                ch_atividade_obrigatoria = row[18] if row[18] != '' else None
                cr_minimo_semestre = row[19] if row[19] != '' else None
                cr_ideal_semestre = row[20] if row[20] != '' else None
                cr_maximo_semestre = row[21] if row[21] != '' else None
                ch_minima_semestre = row[22] if row[22] != '' else None
                ch_ideal_semestre = row[23] if row[23] != '' else None
                ch_maxima_semestre = row[24] if row[24] != '' else None
                periodo_entrada_vigor = row[25] if row[25] != '' else None
                ano_entrada_vigor = row[26] if row[26] != '' else None
                observacao = row[27]

                ec = EstruturaCurricular(id_curriculo=id_curriculo, codigo=codigo, nome=nome_matriz,
                                         semestre_conclusao_minimo=semestre_conclusao_minimo,
                                         semestre_conclusao_ideal=semestre_conclusao_ideal,
                                         semestre_conclusao_maximo=semestre_conclusao_maximo,
                                         meses_conclusao_minimo=meses_conclusao_minimo,
                                         meses_conclusao_ideal=meses_conclusao_ideal,
                                         meses_conclusao_maximo=meses_conclusao_maximo,
                                         cr_total_minimo=cr_total_minimo, ch_total_minima=ch_total_minima,
                                         ch_optativas_minima=ch_optativas_minima,
                                         ch_complementar_minima=ch_complementar_minima, max_eletivos=max_eletivos,
                                         ch_nao_atividade_obrigatoria=ch_nao_atividade_obrigatoria,
                                         cr_nao_atividade_obrigatorio=cr_nao_atividade_obrigatorio,
                                         ch_atividade_obrigatoria=ch_atividade_obrigatoria,
                                         cr_minimo_semestre=cr_minimo_semestre,
                                         cr_ideal_semestre=cr_ideal_semestre, cr_maximo_semestre=cr_maximo_semestre,
                                         ch_minima_semestre=ch_minima_semestre, ch_ideal_semestre=ch_ideal_semestre,
                                         ch_maxima_semestre=ch_maxima_semestre,
                                         periodo_entrada_vigor=periodo_entrada_vigor,
                                         ano_entrada_vigor=ano_entrada_vigor, observacao=observacao, curso=curso_ceres)
                ec.save()


def organizacao():
    print("Criando Estruturas Curriculares para os Cursos do CERES ...!")

    with open('curriculo-componente-graduacao.csv') as csvfile:
        ccg = csv.reader(csvfile, delimiter=';')
        next(ccg)  # skip header

        for row in ccg:

            id_estrutura = row[1]
            id_componente_curricular = row[2]

            if EstruturaCurricular.objects.filter(id_curriculo=id_estrutura).exists():
                ec = EstruturaCurricular.objects.get(id_curriculo=id_estrutura)

                if ComponenteCurricular.objects.filter(id_componente=id_componente_curricular).exists():
                    cc = ComponenteCurricular.objects.get(id_componente=id_componente_curricular)

                    id_curriculo_componente = row[0]
                    id_curriculo = row[1]
                    id_componente_curricular = row[2]
                    semestre_oferta = row[3]
                    tipo_vinculo_componente = row[4]
                    nivel_ensino = row[5]

                    oc = OrganizacaoCurricular(id_curriculo_componente=id_curriculo_componente, estrutura=ec,
                                           componente=cc, semestre=semestre_oferta,
                                           tipo_vinculo=tipo_vinculo_componente, nivel=nivel_ensino)
                    oc.save()


if __name__ == "__main__":
    main()
