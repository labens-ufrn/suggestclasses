from core.models import Docente


def get_docente_by_siape(siape):
    docente = None
    if siape != '' and Docente.objects.filter(siape=siape).exists():
        # Professores Substitutos e Temporários não estão na lista
        docente = Docente.objects.get(siape=siape)
    return docente


def get_docente_by_nome(nome):
    docente = None
    if nome != '' and Docente.objects.filter(nome=nome).exists():
        docente = Docente.objects.get(nome=nome)
    return docente
