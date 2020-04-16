from django.db.models import Q

from core.models import Discente


def get_discentes():
    """
        Lista todos os discentes. Retorna apenas discentes do CERES.
    """
    return Discente.objects.all()


def get_discentes_ativos():
    """
            Lista dos discentes com Status ATIVO. Retorna apenas discentes ativos do CERES.
    """
    query = Q(status='ATIVO')
    query.add(Q(status='ATIVO - FORMANDO'), Q.OR)
    return Discente.objects.filter(query)
