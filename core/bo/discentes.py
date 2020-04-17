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


def get_discente_by_matricula(matricula):
    """
        Retorna um discente dada sua matrícula siape.
    :param matricula: Matrícula do discente.
    :return: Um objeto da classe @Discente.
    """
    discente = None
    if matricula != '' and Discente.objects.filter(matricula=matricula).exists():
        # Professores Substitutos e Temporários não estão na lista
        discente = Discente.objects.get(matricula=matricula)
    return discente
