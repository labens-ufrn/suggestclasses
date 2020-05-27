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


def get_estrutura_by_id(id_estrutura):
    estrutura = None
    if EstruturaCurricular.objects.filter(id_curriculo=id_estrutura).exists():
        estrutura = EstruturaCurricular.objects.get(id_curriculo=id_estrutura)
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
