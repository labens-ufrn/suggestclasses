from core.bo.sevices import get_estrutura_by_id
from core.models import OrganizacaoCurricular, ComponenteCurricular


def get_estrutura_sistemas():
    id_ec = 510230607
    bsi_ec = get_estrutura_by_id(id_ec)
    return bsi_ec


def get_estrutura_sistemas_dct():
    id_ec = 510230608
    bsi_ec = get_estrutura_by_id(id_ec)
    return bsi_ec


