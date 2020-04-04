from core.models import Docente


def get_docentes():
    """
        Lista todos os docentes efetivos. Retorna apenas docentes do CERES.
    """
    return Docente.objects.all()


def get_docente_by_siape(siape):
    """
        Retorna um docente dada sua matrícula siape.
    :param siape: Matrícula siape do docente.
    :return: Um objeto da classe @Docente.
    """
    docente = None
    if siape != '' and Docente.objects.filter(siape=siape).exists():
        # Professores Substitutos e Temporários não estão na lista
        docente = Docente.objects.get(siape=siape)
    return docente


def get_docente_by_nome(nome):
    """
        Retorna um docente dado seu nome.
    :param nome: O nome completo do docente.
    :return: Um objeto da classe @Docente.
    """
    docente = None
    if nome != '' and Docente.objects.filter(nome=nome).exists():
        docente = Docente.objects.get(nome=nome)
    return docente
