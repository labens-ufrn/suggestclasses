from core.bo.sevices import get_estrutura_by_id


def get_estrutura_matematica():
    id_ec = 89214922
    mat_ec = get_estrutura_by_id(id_ec)
    return mat_ec
