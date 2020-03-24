from core.bo.sevices import get_oc_by_semestre
from core.models import Turma, Horario, SugestaoTurma


def get_turmas(estrutura, semestre):
    org_curricular = get_oc_by_semestre(estrutura, semestre)

    turmas = []
    for oc in org_curricular:
        turma = Turma.objects.filter(componente=oc.componente, ano=2019, periodo=2)
        for t in turma:
            turmas.append(t)

    return turmas


def get_sugestao_turmas(estrutura, semestre, ano, periodo):
    org_curricular = get_oc_by_semestre(estrutura, semestre)

    turmas = []
    for oc in org_curricular:
        turma = SugestaoTurma.objects.filter(componente=oc.componente, ano=ano, periodo=periodo)
        for t in turma:
            turmas.append(t)

    return turmas


def get_turmas_por_horario(turmas, dia, turno, ordem):
    turmas_horario = []
    horario = Horario(dia=str(dia), turno=turno, ordem=str(ordem))
    for t in turmas:
        print('Desc Horário: ' + t.descricao_horario)
        desc_horario = t.descricao_horario
        if desc_horario == '':
            print('Turma sem Horário: ' + t.componente.nome)
        horarios = converte_desc_horario(descricao_horario=desc_horario, turno=get_turno(desc_horario))

        if desc_horario != "" and horarios.__contains__(horario):
            turmas_horario.append(t)
    return turmas_horario


def converte_desc_horario(descricao_horario, turno):
    horarios_list = []
    # Trata descricao_horario vazia e turno None.
    if descricao_horario == '' or turno is None:
        return horarios_list

    horario_split = descricao_horario.split(turno)
    dias = horario_split[0]
    ordens = horario_split[1]
    for d in dias:
        for o in ordens:
            horario = Horario(dia=str(d), turno=turno, ordem=str(o))
            horarios_list.append(horario)
    return horarios_list


def get_turno(horario):
    if 'M' in horario:
        return 'M'
    if 'T' in horario:
        return 'T'
    if 'N' in horario:
        return 'N'
    return None


def carrega_turmas(estrutura, periodos):
    turmas = []
    for s in periodos:
        ts = get_turmas(estrutura, s)
        turmas.extend(ts)
    return turmas


def carrega_sugestao_turmas(estrutura, semestres, ano, periodo):
    turmas = []
    for s in semestres:
        ts = get_sugestao_turmas(estrutura, s, ano, periodo)
        turmas.extend(ts)
    return turmas


def carrega_turmas_horario(turmas, turno):
    tt = []
    n = 7
    if turno == 'N':
        n = 5

    for i in range(1, n):
        horario = Horario.objects.filter(turno=turno, ordem=i).order_by('dia')
        turma_horarios = []
        for h in horario:
            turmas_por_horario = get_turmas_por_horario(turmas=turmas, dia=h.dia, turno=turno, ordem=i)
            th = TurmaHorario(h, turmas_por_horario)
            turma_horarios.append(th)
        tt.append(turma_horarios)
    return tt


class TurmaHorario:

    def __init__(self, horario, turmas):
        # salva os dados  que foram passados
        self.turmas = turmas
        self.horario = horario
