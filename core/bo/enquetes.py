from core.bo.sevices import get_oc_by_semestre, get_cc_by_estrutura, get_estrutura_by_curso, get_cc_obrigatorias, \
    get_cc_optativos
from core.models import Enquete
from enum import Enum


class TipoEnquete(Enum):
    COMPLETA = "1"
    OBRIGATORIAS = "2"
    OPTATIVAS = "3"
    PARCIAL = "4"


def get_enquetes():
    """
        Lista todas as Enquetes.
    """
    return Enquete.objects.all().order_by('status', 'curso', '-periodo', '-data_hora_inicio', 'nome')


def get_enquetes_por_curso(curso_id=None):
    """
        Lista todos as Enquetes.
    """
    return Enquete.objects.filter(curso__codigo=curso_id)\
            .order_by('status', 'curso', 'periodo', '-data_hora_inicio', 'nome')


def get_componentes_enquete(enquete):
    estrutura = get_estrutura_by_curso(enquete.curso)
    if TipoEnquete(enquete.tipo) == TipoEnquete.OBRIGATORIAS:
        componentes = get_cc_obrigatorias(estrutura)
    elif TipoEnquete(enquete.tipo) == TipoEnquete.OPTATIVAS:
        componentes = get_cc_optativos(estrutura)
    elif TipoEnquete(enquete.tipo) == TipoEnquete.PARCIAL:
        componentes = get_cc_by_estrutura(estrutura)
    else:
        componentes = get_cc_by_estrutura(estrutura)
    return componentes
