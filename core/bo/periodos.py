from django.db.models import Q

from core.models import PeriodoLetivo


def get_periodo_letivo(status, ano=None, periodo=None):
    query = Q(status=status)
    if ano:
        query.add(Q(ano=ano), Q.AND)
    if periodo:
        query.add(Q(periodo=periodo), Q.AND)
    return PeriodoLetivo.objects.filter(query)


def get_periodo_planejado():
    periodos = get_periodo_letivo(status=PeriodoLetivo.PLANEJADO)
    periodo_letivo = periodos.first()
    return periodo_letivo


def get_periodo_ativo():
    periodos = get_periodo_letivo(status=PeriodoLetivo.ATIVO)
    periodo_letivo = periodos.first()
    return periodo_letivo
