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
    criar_horarios_turno_sabado('M')
    criar_horarios_turno_sabado('T')
    criar_horarios_turno_sabado('N')


def criar_horarios_turno(turno):
    n = 7
    if turno == 'N':
        n = 5

    for d in range(2, 7):
        for i in range(1, n):
            if not Horario.objects.filter(dia=d, turno=turno, ordem=i,
                                          hora_inicio=get_horario_inicio(turno, i),
                                          hora_final=get_horario_final(turno, i)).exists():
                Horario.objects.create(dia=d, turno=turno, ordem=i,
                                       hora_inicio=get_horario_inicio(turno, i),
                                       hora_final=get_horario_final(turno, i))
            else:
                print(Horario.objects.get(dia=d, turno=turno, ordem=i))


def criar_horarios_turno_sabado(turno):
    n = 7
    if turno != 'N':
        for d in range(7, 8):
            for i in range(1, n):
                if not Horario.objects.filter(dia=d, turno=turno, ordem=i,
                                              hora_inicio=get_horario_inicio(turno, i),
                                              hora_final=get_horario_final(turno, i)).exists():
                    Horario.objects.create(dia=d, turno=turno, ordem=i,
                                           hora_inicio=get_horario_inicio(turno, i),
                                           hora_final=get_horario_final(turno, i))
                else:
                    print(Horario.objects.get(dia=d, turno=turno, ordem=i))

    if turno == 'N':
        hora_inicio = time(22, 15, 00)
        hora_final = time(22, 55, 00)
        if not Horario.objects.filter(dia=6, turno=turno, ordem=5,
                                      hora_inicio=hora_inicio,
                                      hora_final=hora_final).exists():
            Horario.objects.create(dia=6, turno=turno, ordem=5,
                                   hora_inicio=hora_inicio,
                                   hora_final=hora_final)
        else:
            print(Horario.objects.get(dia=6, turno=turno, ordem=5))
        hora_inicio = time(18, 45, 00)
        hora_final = time(19, 35, 00)
        if not Horario.objects.filter(dia=7, turno=turno, ordem=1,
                                      hora_inicio=hora_inicio,
                                      hora_final=hora_final).exists():
            Horario.objects.create(dia=7, turno=turno, ordem=1,
                                   hora_inicio=hora_inicio,
                                   hora_final=hora_final)
        else:
            print(Horario.objects.get(dia=7, turno=turno, ordem=1))
        hora_inicio = time(19, 35, 00)
        hora_final = time(20, 25, 00)
        if not Horario.objects.filter(dia=7, turno=turno, ordem=2,
                                      hora_inicio=hora_inicio,
                                      hora_final=hora_final).exists():
            Horario.objects.create(dia=7, turno=turno, ordem=2,
                                   hora_inicio=hora_inicio,
                                   hora_final=hora_final)
        else:
            print(Horario.objects.get(dia=7, turno=turno, ordem=2))


def get_horario_inicio(turno, ordem):
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
    if turno == 'N' and ordem == 1:
        hora_inicio = time(18, 45, 00)
    if turno == 'N' and ordem == 2:
        hora_inicio = time(19, 35, 00)
    if turno == 'N' and ordem == 3:
        hora_inicio = time(20, 35, 00)
    if turno == 'N' and ordem == 4:
        hora_inicio = time(21, 25, 00)
    return hora_inicio


def get_horario_final(turno, ordem):
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
    if turno == 'N' and ordem == 1:
        hora_final = time(19, 35, 00)
    if turno == 'N' and ordem == 2:
        hora_final = time(20, 25, 00)
    if turno == 'N' and ordem == 3:
        hora_final = time(21, 25, 00)
    if turno == 'N' and ordem == 4:
        hora_final = time(22, 15, 00)
    return hora_final


if __name__ == "__main__":
    main()
