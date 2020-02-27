from core.bo.sevices import get_oc_by_semestre
from core.models import Turma, Horario


def get_turmas(estrutura, semestre):
    org_curricular = get_oc_by_semestre(estrutura, semestre)

    turmas = []
    for oc in org_curricular:
        turma = Turma.objects.filter(componente=oc.componente, ano=2019, periodo=2)
        for t in turma:
            turmas.append(t)

    return turmas


def get_turmas_por_horario(turmas, dia, turno, ordem):
    turmas_horario = []
    horario = Horario(dia=str(dia), turno=turno, ordem=str(ordem))
    for t in turmas:
        print(t)
        print(t.descricao_horario)
        horarios = converte_desc_horario(descricao_horario=t.descricao_horario, turno=get_turno(t.descricao_horario))
        print(horario)
        print(horarios)

        if horarios.__contains__(horario):
            print(t.componente.nome)
            turmas_horario.append(t)
    return turmas_horario


def converte_desc_horario(descricao_horario, turno):
    horarios_list = []
    horario_split = descricao_horario.split(turno)
    dias = horario_split[0]
    ordens = horario_split[1]
    dias_size = len(dias)
    ordens_size = len(ordens)
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

class TurmaHorario:

    def __init__(self, horario, turmas):
        # salva os dados  que foram passados
        self.turmas = turmas
        self.horario = horario
