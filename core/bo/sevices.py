from django.db.models import Sum

from core.models import OrganizacaoCurricular, ComponenteCurricular, EstruturaCurricular


def get_oc_by_semestre(estrutura, semestre):
    return OrganizacaoCurricular.objects.filter(estrutura=estrutura, semestre=semestre)


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
