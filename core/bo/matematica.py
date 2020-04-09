from core.models import EstruturaCurricular


def get_estrutura_matematica():
    id_ec = 89214922
    mat_ec = EstruturaCurricular.objects.get(id_curriculo=id_ec)
    return mat_ec
