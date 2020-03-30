from django.db.models import Sum

from core.models import OrganizacaoCurricular, ComponenteCurricular


def get_oc_by_semestre(estrutura, semestre):
    return OrganizacaoCurricular.objects.filter(estrutura=estrutura, semestre=semestre)


def get_ch_by_semestre(estrutura, semestre):
    return OrganizacaoCurricular.objects.filter(estrutura=estrutura, semestre=semestre)\
        .aggregate(Sum("componente__ch_total"))


def get_cc_by_estrutura(estrutura):
    oc = OrganizacaoCurricular.objects.filter(estrutura=estrutura).values_list('componente', flat=True)
    loc = list(oc)
    componentes = ComponenteCurricular.objects.filter(pk__in=loc)
    return componentes
