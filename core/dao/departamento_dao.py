from core.models import Departamento


def get_departamentos():
    """
        Lista todos os departamentos. Retorna apenas departamentos do CERES.
    """
    return Departamento.objects.all()


def get_depto_by_id(id_depto):
    return Departamento.objects.get(id_unidade=id_depto)


def get_dct():
    """
        Retorna apenas o departamento DCT.
    """
    id_dct = 9726
    return get_depto_by_id(id_dct)
