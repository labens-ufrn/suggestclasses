from core.models import Discente


def get_discentes():
    """
        Lista todos os discentes. Retorna apenas discentes do CERES.
    """
    return Discente.objects.all()
