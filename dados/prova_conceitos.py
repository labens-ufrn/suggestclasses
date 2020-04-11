import os
from datetime import datetime, date

import django

from mysite.settings import BASE_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from core.bo.sistemas import get_estrutura_sistemas, criar_organizacao_sistemas_dct, get_estrutura_sistemas_dct
from core.bo.turma import get_turmas, converte_desc_horario, TurmaHorario, get_turmas_por_horario
from core.models import Horario, FuncaoGratificada


def main():
    print("Executável para testes de conceitos e ideias!")
    print(os.getcwd())
    print('BASE_DIR')
    print(BASE_DIR)

    hoje = date.today()

    fgs = FuncaoGratificada.objects.all()
    fg_taciano = FuncaoGratificada.objects.filter(siape=1721652, inicio__lte=hoje, fim__gt=hoje)
    fg_ronny = FuncaoGratificada.objects.filter(siape=1789459, inicio__lte=hoje, fim__gt=hoje)
    fg_flavius = FuncaoGratificada.objects.filter(siape=1687186, inicio__lte=hoje, fim__gt=hoje)
    fg_almir = FuncaoGratificada.objects.filter(siape=12746, inicio__lte=hoje, fim__gt=hoje)
    fg_humberto = FuncaoGratificada.objects.filter(siape=1196714, inicio__lte=hoje, fim__gt=hoje)

    for fg in fg_taciano:
        print(fg.atividade, fg.inicio, fg.fim)
    for fg in fg_ronny:
        print(fg.atividade, fg.inicio, fg.fim)
    for fg in fg_flavius:
        print(fg.atividade, fg.inicio, fg.fim)
    for fg in fg_almir:
        print(fg.atividade, fg.inicio, fg.fim)
    for fg in fg_humberto:
        print(fg.atividade, fg.inicio, fg.fim)

    date1 = date(2014, 3, 2)
    date2 = date(2013, 8, 1)
    was_date1_before = date1 < date2 # Check if date1 is before date2
    print(was_date1_before)

    # criar_organizacao_sistemas_dct()

    # bsi_dct = get_estrutura_sistemas_dct()
    #
    # semestre = 1
    # turmas1p = get_turmas(bsi_dct, semestre, ano=2019, periodo=2)
    #
    # for t in turmas1p:
    #     print('Turma: ' + t.__str__())
    #     print(t)
    #
    # # Criar objeto para guardar Horário e Turmas;
    # turma_horarios = []
    # for i in range(1, 7):
    #     horario = Horario.objects.filter(turno='M', ordem=i).order_by('dia')
    #     for h in horario:
    #         turmas = get_turmas_por_horario(turmas=turmas1p, dia=h.dia, turno='M', ordem=i)
    #         th = TurmaHorario(h, turmas)
    #         turma_horarios.append(th)
    #
    # for i in range(1, 7):
    #     horario = Horario.objects.filter(turno='T', ordem=i).order_by('dia')
    #     for h in horario:
    #         turmas = get_turmas_por_horario(turmas=turmas1p, dia=h.dia, turno='T', ordem=i)
    #         th = TurmaHorario(h, turmas)
    #         turma_horarios.append(th)
    #
    # for tur_hor in turma_horarios:
    #     print(tur_hor)
    #
    # # get_turmas(bsi_dct, 2)


if __name__ == "__main__":
    main()
