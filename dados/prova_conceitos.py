import os
from datetime import datetime, date
from mysite.settings import BASE_DIR
import django
django.setup()
from core.models import Horario, FuncaoGratificada

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


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


if __name__ == "__main__":
    main()
