from core.bo.sevices import get_estrutura_by_id


def get_estrutura_pedagogia():
    id_ec = 133495154
    ped_ec = get_estrutura_by_id(id_ec)
    return ped_ec
