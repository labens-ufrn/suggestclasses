from typing import List
from django.shortcuts import render
from core.bo.sevices import get_oc_by_semestre, get_ch_by_semestre


def flow_horizontal(request, estrutura, link_opcionais):
    """
    Função que monta o contexto para a telas que Exibe a Estrutura Curricular na Horizontal.
    :param request: Uma Requisição HTTP.
    :param estrutura: Um objeto do tipo @EstruturaCurricular.
    :return: Um Response HTTP.
    """
    headers: List[str] = []
    estrutura_all = []
    max_comp_by_semestre = 0
    for s in range(1, 9):
        estrutura_row = []
        oc = get_oc_by_semestre(estrutura, s)
        ch = get_ch_by_semestre(estrutura, s)

        num_comp_by_semestre = len(oc)
        if num_comp_by_semestre >= max_comp_by_semestre:
            max_comp_by_semestre = num_comp_by_semestre

        estrutura_row.append(f"{s}º")
        estrutura_row.append(oc)
        estrutura_row.append(num_comp_by_semestre)
        estrutura_row.append(ch)
        estrutura_all.append(estrutura_row)

    # Ajustando a diferença entre do número de componentes no semestre e o máximo.
    for row in estrutura_all:
        row[2] = max_comp_by_semestre - row[2]

    context = {
        'estrutura': estrutura,
        'max_comp_by_semestre': max_comp_by_semestre,
        'estrutura_all': estrutura_all,
        'link_opcionais': link_opcionais,
    }

    return render(request, 'core/flow/flow-horizontal.html', context)


def flow_bsi_op(request, estrutura):
    estrutura_opcionais = get_oc_by_semestre(estrutura, 0)

    context = {
        'estrutura_opcionais': estrutura_opcionais,
    }
