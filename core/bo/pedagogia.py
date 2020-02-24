from core.models import EstruturaCurricular


def get_estrutura_pedagogia():
    id_ec = 133495154
    ped_ec = EstruturaCurricular.objects.get(id_curriculo=id_ec)
    return ped_ec
