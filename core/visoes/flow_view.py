from django.shortcuts import render
from core.bo.sevices import get_oc_by_semestre, get_ch_by_semestre, get_estrutura_direito, get_estrutura_matematica, \
    get_estrutura_pedagogia, get_estrutura_administracao, get_estrutura_turismo, get_estrutura_letras_portugues, \
    get_estrutura_letras_espanhol, get_estrutura_letras_ingles, get_estrutura_contabeis, \
    get_estrutura_historia_licenciatura, get_estrutura_historia_bacharelado
from core.bo.sistemas import get_estrutura_sistemas_dct


def flow_horizontal(request, estrutura, link_opcionais):
    """
    Função que monta o contexto para a telas que Exibe a Estrutura Curricular na Horizontal.
    :param link_opcionais: Link para os componentes opcionais da Estrutura Curricular.
    :param request: Uma Requisição HTTP.
    :param estrutura: Um objeto do tipo @EstruturaCurricular.
    :return: Um Response HTTP.
    """
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


def flow_opcionais(request, estrutura):
    semestre_opcional = 0
    estrutura_opcionais = get_oc_by_semestre(estrutura, semestre_opcional)

    context = {
        'estrutura': estrutura,
        'estrutura_opcionais': estrutura_opcionais,
    }

    return render(request, 'core/flow/flow-opcionais.html', context)


def carrega_context_flow_list():
    """
    Carrega todas as Estruturas Curriculares do centro CERES.
    """
    cont_flow = get_estrutura_contabeis()
    dir_flow = get_estrutura_direito()
    bsi_flow = get_estrutura_sistemas_dct()
    ped_flow = get_estrutura_pedagogia()
    mat_flow = get_estrutura_matematica()
    adm_flow = get_estrutura_administracao()
    tur_flow = get_estrutura_turismo()
    let_por_flow = get_estrutura_letras_portugues()
    let_esp_flow = get_estrutura_letras_espanhol()
    let_ing_flow = get_estrutura_letras_ingles()
    his_lic_flow = get_estrutura_historia_licenciatura()
    his_bac_flow = get_estrutura_historia_bacharelado()

    context = {
        'cont_flow': cont_flow,
        'dir_flow': dir_flow,
        'mat_flow': mat_flow,
        'ped_flow': ped_flow,
        'bsi_flow': bsi_flow,
        'adm_flow': adm_flow,
        'tur_flow': tur_flow,
        'let_por_flow': let_por_flow,
        'let_esp_flow': let_esp_flow,
        'let_ing_flow': let_ing_flow,
        'his_lic_flow': his_lic_flow,
        'his_bac_flow': his_bac_flow,
    }

    return context
