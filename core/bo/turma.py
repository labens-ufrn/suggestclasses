from core.bo.sevices import get_oc_by_semestre
from core.models import Turma


def get_turmas(estrutura, semestre):
    org_curricular = get_oc_by_semestre(estrutura, semestre)

    turmas = []
    for oc in org_curricular:
        turma = Turma.objects.filter(componente=oc.componente, ano=2019, periodo=2)
        for t in turma:
            turmas.append(t)

    return turmas


def get_turmas_por_horario(turmas, ordem, turno, dia):
    turmas_nomes = []

    for t in turmas:
        print('Turma: ' + t.__str__())
        print('ordem: ' + ordem.__str__() + ' turno: ' + turno.__str__() + ' dia: ' + dia.__str__())
        print(t.descricao_horario)
        horario = t.descricao_horario.split(turno)
        print(horario)

        if turno in t.descricao_horario and ordem.__str__() in horario[1] and  dia in horario[0]:
            print(t.componente.nome)
            turmas_nomes.append(t.componente.nome)
    return turmas_nomes
