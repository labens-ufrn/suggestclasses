import os
import csv
import django
from dateutil.parser import parse
django.setup()

from core.models import Departamento, Docente
from mysite.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')


def main():
    os.chdir(DADOS_PATH)
    carregar_docentes()


def carregar_docentes():
    print("\nCriando Docentes do CERES ...!")

    with open('docentes.csv') as csvfile:
        docentes = csv.reader(csvfile, delimiter=';')
        next(docentes)  # skip header

        for row in docentes:
            carregar_docente(row)
        print()


def carregar_docente(row):
    siape = row[0]
    nome = row[1]
    sexo = row[2]
    formacao = row[3]
    tipo_jornada_trabalho = row[4]
    vinculo = row[5]
    categoria = row[6]
    classe_funcional = row[7]
    id_unidade_lotacao = row[8]
    lotacao = row[9]
    admissao_str = row[10]
    # https://stackabuse.com/converting-strings-to-datetime-in-python/
    admissao = parse(admissao_str)

    if id_unidade_lotacao == '1482' or Departamento.objects.filter(id_unidade=id_unidade_lotacao).exists():

        depto = None
        if Departamento.objects.filter(id_unidade=id_unidade_lotacao).exists():
            depto = Departamento.objects.get(id_unidade=id_unidade_lotacao)
        else:
            print(siape)
            print(nome)
            print(lotacao)

        if not Docente.objects.filter(siape=siape).exists():
            print("Adicionando Docente: " + siape + " - " + nome)
            professor = Docente(siape=siape, nome=nome, sexo=sexo, formacao=formacao,
                                tipo_jornada_trabalho=tipo_jornada_trabalho,
                                vinculo=vinculo, categoria=categoria, classe_funcional=classe_funcional,
                                id_unidade_lotacao=id_unidade_lotacao, lotacao=lotacao, admissao=admissao,
                                departamento=depto)
            professor.save()
            print('+', end="")
        else:
            docente = Docente.objects.get(siape=siape)
            if docente.departamento is None:
                docente.departamento = depto
                docente.save()
                print('.', end="")


if __name__ == "__main__":
    main()
