import django
django.setup()
from django import db
from datetime import time
from core.models import Horario


def main():
    print("Povoar Horários da UFRN!")
    # print(db.connections.databases)
    povoar_horarios()


def povoar_horarios():
    criar_horarios_turno('M')
    criar_horarios_turno('T')
    criar_horarios_turno('N')


def criar_horarios_turno(turno):
    dias = 8
    ordens = 7
    if turno == 'N':
        ordens = 6

    # d (dia) vai de segunda até sábado, o range usa o intervalo [2,8)
    # i (ordem) vai do 1º horário até o 6º horário, o range usa o intervalo [1,7)
    for d in range(2, dias):
        for i in range(1, ordens):
            if not Horario.objects.filter(
                dia=d, turno=turno, ordem=i,
                hora_inicio=get_horario_inicio(turno, i),
                hora_final=get_horario_final(turno, i)).exists():

                    Horario.objects.create(
                        dia=d, turno=turno, ordem=i,                     hora_inicio=get_horario_inicio(turno, i),
                        hora_final=get_horario_final(turno, i))
                    print('+', end="")
            else:
                print('.', end="")


def get_horario_inicio(turno, ordem):
    hora_inicio = None
    if turno == 'M':
        hora_inicio = get_horario_inicio_manha(turno, ordem)
    if turno == 'T':
        hora_inicio = get_horario_inicio_tarde(turno, ordem)
    if turno == 'N':
        hora_inicio = get_horario_inicio_noite(turno, ordem)
    return hora_inicio


def get_horario_inicio_manha(turno, ordem):
    hora_inicio = None
    if turno == 'M' and ordem == 1:
        hora_inicio = time(7, 00, 00)
    if turno == 'M' and ordem == 2:
        hora_inicio = time(7, 50, 00)
    if turno == 'M' and ordem == 3:
        hora_inicio = time(8, 55, 00)
    if turno == 'M' and ordem == 4:
        hora_inicio = time(9, 45, 00)
    if turno == 'M' and ordem == 5:
        hora_inicio = time(10, 50, 00)
    if turno == 'M' and ordem == 6:
        hora_inicio = time(11, 40, 00)
    return hora_inicio

def get_horario_inicio_tarde(turno, ordem):
    hora_inicio = None
    if turno == 'T' and ordem == 1:
        hora_inicio = time(13, 00, 00)
    if turno == 'T' and ordem == 2:
        hora_inicio = time(13, 50, 00)
    if turno == 'T' and ordem == 3:
        hora_inicio = time(14, 55, 00)
    if turno == 'T' and ordem == 4:
        hora_inicio = time(15, 45, 00)
    if turno == 'T' and ordem == 5:
        hora_inicio = time(16, 50, 00)
    if turno == 'T' and ordem == 6:
        hora_inicio = time(17, 40, 00)
    return hora_inicio

def get_horario_inicio_noite(turno, ordem):
    hora_inicio = None
    if turno == 'N' and ordem == 1:
        hora_inicio = time(18, 45, 00)
    if turno == 'N' and ordem == 2:
        hora_inicio = time(19, 35, 00)
    if turno == 'N' and ordem == 3:
        hora_inicio = time(20, 35, 00)
    if turno == 'N' and ordem == 4:
        hora_inicio = time(21, 25, 00)
    if turno == 'N' and ordem == 4:
        hora_inicio = time(21, 25, 00)
    if turno == 'N' and ordem == 5:
        hora_inicio = time(22, 15, 00)
    return hora_inicio


def get_horario_final(turno, ordem):
    hora_final = None
    if turno == 'M':
        hora_final = get_horario_final_manha(turno, ordem)
    if turno == 'T':
        hora_final = get_horario_final_tarde(turno, ordem)
    if turno == 'N':
        hora_final = get_horario_final_noite(turno, ordem)
    return hora_final

def get_horario_final_manha(turno, ordem):
    hora_final = None
    if turno == 'M' and ordem == 1:
        hora_final = time(7, 50, 00)
    if turno == 'M' and ordem == 2:
        hora_final = time(8, 40, 00)
    if turno == 'M' and ordem == 3:
        hora_final = time(9, 45, 00)
    if turno == 'M' and ordem == 4:
        hora_final = time(10, 35, 00)
    if turno == 'M' and ordem == 5:
        hora_final = time(11, 40, 00)
    if turno == 'M' and ordem == 6:
        hora_final = time(12, 30, 00)
    return hora_final

def get_horario_final_tarde(turno, ordem):
    hora_final = None
    if turno == 'T' and ordem == 1:
        hora_final = time(13, 50, 00)
    if turno == 'T' and ordem == 2:
        hora_final = time(14, 40, 00)
    if turno == 'T' and ordem == 3:
        hora_final = time(15, 45, 00)
    if turno == 'T' and ordem == 4:
        hora_final = time(16, 35, 00)
    if turno == 'T' and ordem == 5:
        hora_final = time(17, 40, 00)
    if turno == 'T' and ordem == 6:
        hora_final = time(18, 30, 00)
    return hora_final

def get_horario_final_noite(turno, ordem):
    hora_final = None
    if turno == 'N' and ordem == 1:
        hora_final = time(19, 35, 00)
    if turno == 'N' and ordem == 2:
        hora_final = time(20, 25, 00)
    if turno == 'N' and ordem == 3:
        hora_final = time(21, 25, 00)
    if turno == 'N' and ordem == 4:
        hora_final = time(22, 15, 00)
    if turno == 'N' and ordem == 5:
        hora_final = time(23, 5, 00)
    return hora_final


if __name__ == "__main__":
    main()
