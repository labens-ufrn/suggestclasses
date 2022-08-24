from django.db.models import Q

from core.models import Centro, Curso, Discente


def get_discentes():
    """
        Lista todos os discentes. Retorna apenas discentes do CERES.
    """
    return Discente.objects.all()

def get_discentes_by_centro(centro: Centro):
    """
        Lista todos os discentes de um centro.
    """
    if centro:
        return Discente.objects.filter(id_unidade=centro.id_unidade)
    return get_discentes()

def get_discentes_ativos(curso: Curso = None, centro: Centro = None):
    """
            Lista dos discentes com Status ATIVO. Retorna apenas discentes ativos do CERES.
    """
    query = Q(status='ATIVO')
    query.add(Q(status='ATIVO - FORMANDO'), Q.OR)

    if curso:
        query.add(Q(id_curso=curso.codigo), Q.AND)

    if centro:
        query.add(Q(id_unidade=centro.id_unidade), Q.AND)

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


def get_qtd_discentes_ativos(curso=None):
    return get_discentes_ativos(curso).all().count()
