from dateutil.parser import parse

from core.bo.docente import get_docente_by_siape
from core.models import Docente, FuncaoGratificada


def carregar_funcoes_gratificadas(row):
    siape = row[0] if row[0] != '' else None

    if Docente.objects.filter(siape=siape).exists():
        docente = get_docente_by_siape(siape)

        nome = row[1]
        situacao_servidor = row[2]
        id_unidade = row[3]
        lotacao = row[4]
        sigla = row[5]
        inicio = parse(row[6]) if row[6] != '' else None
        fim = parse(row[7]) if row[7] != '' else None
        id_unidade_designacao = row[8]
        unidade_designacao = row[9]
        atividade = row[10]
        observacoes = row[11]
        print(siape)
        print(inicio)
        print(fim)
        if not FuncaoGratificada.objects.filter(
           siape=siape, id_unidade=id_unidade, inicio=inicio, atividade=atividade).exists():
            print("Adicionando FuncaoGratificada " + siape + " - " + id_unidade + "- " + inicio.__str__() + " - " + atividade)
            fg = FuncaoGratificada(siape=siape, nome=nome, situacao_servidor=situacao_servidor,
                                   id_unidade=id_unidade, lotacao=lotacao, sigla=sigla,
                                   inicio=inicio, fim=fim, id_unidade_designacao=id_unidade_designacao,
                                   unidade_designacao=unidade_designacao, atividade=atividade,
                                   observacoes=observacoes)
            fg.save()
        else:
            print('.', end="")
