from core.dao.departamento_dao import get_dct
from core.models import ComponenteCurricular


def get_componentes_curriculares():
    """
        Lista todos os componentes curriculares.
    """
    return ComponenteCurricular.objects.all()


def get_componentes_by_depto(depto):
    """
        Lista todos os componentes de um departamento.
    """
    return ComponenteCurricular.objects.filter(departamento=depto)


def get_componentes_dct():
    """
         Retorna apenas componentes do departamento DCT.
        :return:
    """
    dct = get_dct()
    componentes_dct = get_componentes_by_depto(dct)
    return componentes_dct
