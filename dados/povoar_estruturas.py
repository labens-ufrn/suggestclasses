import os
import csv
import django
django.setup()
from core.models import Curso, EstruturaCurricular
from dados.service.estrutura_service import STATUS_ATIVA, atualizar_estrutura
from dados.service.util import gravar_arquivo
from suggestclasses.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')

estruturas_atualizadas_list = list()


def main():
    os.chdir(DADOS_PATH)
    print("\nCriando Estruturas Curriculares do CERES ...!")
    carregar_estruturas()


def carregar_estruturas():
    with open('csv/estruturas-curriculares.csv') as csvfile:
        estruturas_ceres = csv.reader(csvfile, delimiter=';')
        next(estruturas_ceres)  # skip header

        for row in estruturas_ceres:
            carregar_estrutura(row)
        print()

    if estruturas_atualizadas_list:
        gravar_arquivo('estruturas_atualizadas', estruturas_atualizadas_list)

def carregar_estrutura(row):
    curso_ufrn = row[3]

    if Curso.objects.filter(codigo=curso_ufrn).exists():
        curso_ceres = Curso.objects.get(codigo=curso_ufrn)
        ec = criar_estrutura(row, curso_ceres)

        if not EstruturaCurricular.objects.filter(id_curriculo=ec.id_curriculo).exists():
            print("Adicionando Estrutura: " + ec.id_curriculo + " - " + ec.codigo + " - " + ec.nome)
            ec.save()
            print('+', end="")
        else:
            estrutura_antiga, atualizacoes = atualizar_estrutura(ec)
            if estrutura_antiga and atualizacoes:
                estruturas_atualizadas_list.append(str(estrutura_antiga) + ', ' + str(atualizacoes))
            else:
                print('.', end="")


def criar_estrutura(row, curso):
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

    ec = EstruturaCurricular(
            id_curriculo=id_curriculo, codigo=codigo, nome=nome_matriz,
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
            cr_minimo_semestre=cr_minimo_semestre, cr_ideal_semestre=cr_ideal_semestre,
            cr_maximo_semestre=cr_maximo_semestre, ch_minima_semestre=ch_minima_semestre,
            ch_ideal_semestre=ch_ideal_semestre, ch_maxima_semestre=ch_maxima_semestre,periodo_entrada_vigor=periodo_entrada_vigor, ano_entrada_vigor=ano_entrada_vigor, observacao=observacao, curso=curso,status=STATUS_ATIVA)
    return ec

if __name__ == "__main__":
    main()
