from core.models import Sala


def get_salas():
    """
        Lista todos as Salas. Retorna apenas salas do CERES.
    """
    return Sala.objects.all().order_by('campus', 'sigla', 'nome')
