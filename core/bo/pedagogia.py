from django.db.models import Sum

from core.models import EstruturaCurricular, OrganizacaoCurricular


def get_estrutura_pedagogia():
    id_ec = 133495154
    ped_ec = EstruturaCurricular.objects.get(id_curriculo=id_ec)
    return ped_ec


def get_oc_by_semestre(estrutura, semestre):
    return OrganizacaoCurricular.objects.filter(estrutura=estrutura, semestre=semestre)


def get_ch_by_semestre(estrutura, semestre):
    return OrganizacaoCurricular.objects.filter(estrutura=estrutura, semestre=semestre)\
        .aggregate(Sum("componente__ch_total"))
