from core.dao.departamento_dao import get_dct
from core.models import Centro, ComponenteCurricular


def get_componentes_curriculares():
    """
        Lista todos os componentes curriculares.
    """
    return ComponenteCurricular.objects.all()

def get_cc_by_centro(centro: Centro):
    """
        Lista os componentes curriculares dos departamentos de um dado centro.
    """
    return ComponenteCurricular.objects.filter(departamento__centro=centro)


def get_componente_by_id(id_componente):
    """
        Retorna um componente curricular pelo id_componente.
    """
    return ComponenteCurricular.objects.get(id_componente=id_componente)


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
