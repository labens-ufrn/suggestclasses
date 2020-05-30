from core.bo.turma import TurmaHorario
from core.models import Docente, FuncaoGratificada, Horario
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


def get_vinculos_docente(docente, horario, ano, periodo):
    turmas_por_horario = horario.vinculos.all().filter(
        docente=docente, turma__ano=ano, turma__periodo=periodo)
    return turmas_por_horario


def carrega_turmas_por_horario(docente, ano, periodo):
    turmas_por_horario = []
    n = 7
    turnos = ['M', 'T', 'N']
    for turno in turnos:
        if turno == 'N':
            n = 5

        for i in range(1, n):
            horarios = Horario.objects.filter(turno=turno, ordem=i).order_by('dia')
            turmas_horario = []
            for h in horarios:
                vinculos_por_horario = \
                    get_vinculos_docente(docente=docente, horario=h, ano=ano, periodo=periodo)
                th = TurmaHorario(h, [])
                for v in vinculos_por_horario:
                    turma = v.turma
                    th = TurmaHorario(h, [turma])
                turmas_horario.append(th)
            turmas_por_horario.append(turmas_horario)
    return turmas_por_horario
