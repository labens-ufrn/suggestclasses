from datetime import datetime

import pytz

from core.models import Centro, Departamento, FuncaoGratificada


def get_departamentos():
    """
        Lista todos os departamentos. Retorna apenas departamentos do CERES.
    """
    return Departamento.objects.all()

def get_deptos_by_centro(centro: Centro):
    """
        Lista os departamentos de um centro.
    """
    return Departamento.objects.filter(centro=centro)

def get_depto_by_id(id_depto):
    return Departamento.objects.get(id_unidade=id_depto)


def get_dct():
    """
        Retorna apenas o departamento DCT.
    """
    id_dct = 9726
    return get_depto_by_id(id_dct)
