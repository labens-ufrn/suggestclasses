from django.db.models import Sum

from core.models import OrganizacaoCurricular, ComponenteCurricular, EstruturaCurricular


def get_oc_by_semestre(estrutura, semestre):
    return OrganizacaoCurricular.objects.filter(estrutura=estrutura, semestre=semestre)


def get_organizacao_by_componente(estrutura, componente):
    return OrganizacaoCurricular.objects.filter(estrutura=estrutura, componente=componente)


def get_ch_by_semestre(estrutura, semestre):
    return OrganizacaoCurricular.objects.filter(estrutura=estrutura, semestre=semestre)\
        .aggregate(Sum("componente__ch_total"))


def get_cc_by_estrutura(estrutura):
    oc = OrganizacaoCurricular.objects.filter(estrutura=estrutura).values_list('componente', flat=True)
    loc = list(oc)
    componentes = ComponenteCurricular.objects.filter(pk__in=loc).order_by('nome', 'codigo')
    return componentes


def get_cc_by_semestre(estrutura, semestre):
    """
    Retorna uma lista de componentes do estrutura para o semestre informado.
    :param estrutura:
    :param semestre:
    :return:
    """
    oc = OrganizacaoCurricular.objects.filter(estrutura=estrutura, semestre=semestre)\
        .values_list('componente', flat=True)
    componentes = ComponenteCurricular.objects.filter(pk__in=oc).order_by('nome', 'codigo')
    return componentes


def get_cc_optativos(estrutura):
    """
    Retorna lista de componentes curriculares optativos da estrutura curricular.
    :param estrutura:
    :return:
    """
    semestre_opcional = 0
    componentes = get_cc_by_semestre(estrutura, semestre_opcional)
    return componentes


def get_cc_obrigatorias(estrutura):
    """
    Retorna lista de componentes curriculares obrigatórios da estrutura curricular.
    :param estrutura:
    :return:
    """
    componentes = get_cc_by_semestre(estrutura, 1)
    for semestre in range(2, 9):
        cc = get_cc_by_semestre(estrutura, semestre)
        # The querysets can be merged using the | operator:
        componentes = componentes | cc
    return componentes


def get_estrutura_by_id(id_estrutura):
    estrutura = None
    if EstruturaCurricular.objects.filter(id_curriculo=id_estrutura).exists():
        estrutura = EstruturaCurricular.objects.get(id_curriculo=id_estrutura)
    return estrutura


def get_estrutura_by_curso(curso):
    estruturas = curso.estruturacurricular_set.all()
    estrutura = estruturas[0]
    if curso.nome == 'SISTEMAS DE INFORMAÇÃO':
        estrutura = estruturas[1]
    return estrutura


def get_estrutura_direito():
    """
    Retorna a Estrutura Curricular ativa do Curso de Direito de Caicó.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 130320907
    dir_ec = get_estrutura_by_id(id_ec)
    return dir_ec


def get_estrutura_matematica():
    id_ec = 89214922
    mat_ec = get_estrutura_by_id(id_ec)
    return mat_ec


def get_estrutura_pedagogia():
    id_ec = 133495154
    ped_ec = get_estrutura_by_id(id_ec)
    return ped_ec


def get_estrutura_administracao():
    """
    Retorna a Estrutura Curricular ativa do Curso de Administração - Currais Novos.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 121631446
    adm_ec = get_estrutura_by_id(id_ec)
    return adm_ec


def get_estrutura_turismo():
    """
    Retorna a Estrutura Curricular ativa do Curso de Turismo - Currais Novos.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 119546991
    turismo_ec = get_estrutura_by_id(id_ec)
    return turismo_ec


def get_estrutura_letras_portugues():
    """
    Retorna a Estrutura Curricular ativa do Curso de Letras - Língua Portuguesa - Currais Novos.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 512507270
    turismo_ec = get_estrutura_by_id(id_ec)
    return turismo_ec


def get_estrutura_letras_ingles():
    """
    Retorna a Estrutura Curricular ativa do Curso de Letras - Português e Inglês - Currais Novos.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 133298488
    turismo_ec = get_estrutura_by_id(id_ec)
    return turismo_ec


def get_estrutura_letras_espanhol():
    """
    Retorna a Estrutura Curricular ativa do Curso de Letras - Língua Espanhola - Currais Novos.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 133506143
    turismo_ec = get_estrutura_by_id(id_ec)
    return turismo_ec


def get_estrutura_contabeis():
    """
    Retorna a Estrutura Curricular ativa do Curso de Ciências Contábeis - Caicó.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 2984610
    contabeis_ec = get_estrutura_by_id(id_ec)
    return contabeis_ec


def get_estrutura_historia_licenciatura():
    """
    Retorna a Estrutura Curricular ativa do Curso de História Licenciatura - Caicó.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 96085436
    historia_licenciatura_ec = get_estrutura_by_id(id_ec)
    return historia_licenciatura_ec


def get_estrutura_historia_bacharelado():
    """
    Retorna a Estrutura Curricular ativa do Curso de História - Bacharelado - Caicó.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 96085636
    historia_bacharelado_ec = get_estrutura_by_id(id_ec)
    return historia_bacharelado_ec


def get_estrutura_geografia_licenciatura():
    """
    Retorna a Estrutura Curricular ativa do Curso de Geografia - Licenciatura - Caicó.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 89189948
    geografia_licenciatura_ec = get_estrutura_by_id(id_ec)
    return geografia_licenciatura_ec


def get_estrutura_geografia_bacharelado():
    """
    Retorna a Estrutura Curricular ativa do Curso de Geografia - Bacharelado - Caicó.
    :return: Um objeto da classe EstruturaCurricular.
    """
    id_ec = 89306921
    geografia_bacharelado_ec = get_estrutura_by_id(id_ec)
    return geografia_bacharelado_ec
