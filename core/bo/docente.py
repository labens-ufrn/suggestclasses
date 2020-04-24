from core.models import Docente, FuncaoGratificada
from datetime import date


def get_docentes():
    """
        Lista todos os docentes efetivos. Retorna apenas docentes do CERES.
    """
    return Docente.objects.all().order_by('nome')


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


def get_funcao_by_siape(siape):
    """
        Retorna as funções gratificadas ativas do docente dada sua matrícula siape.
    :param siape: Matrícula siape do docente.
    :return: Um objeto da classe @FuncaoGratificada.
    """
    funcoes = []
    if siape != '' and Docente.objects.filter(siape=siape).exists():
        docente = Docente.objects.get(siape=siape)
        hoje = date.today()
        if FuncaoGratificada.objects.filter(siape=docente.siape, inicio__lte=hoje, fim__gt=hoje).exists():
            fgs = FuncaoGratificada.objects.filter(siape=docente.siape, inicio__lte=hoje, fim__gt=hoje)
            for fg in fgs:
                funcoes.append(fg)
    return funcoes
