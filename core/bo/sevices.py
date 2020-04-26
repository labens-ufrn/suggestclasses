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
