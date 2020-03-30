from core.models import Docente


def get_docente_by_siape(siape):
    docente = None
    if siape != '' and Docente.objects.filter(siape=siape).exists():
        # Professores Substitutos e Temporários não estão na lista
        docente = Docente.objects.get(siape=siape)
    return docente
