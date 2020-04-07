from core.bo.curriculo import get_curriculo_by_cc
from core.bo.docente import get_docente_by_siape
from core.models import ComponenteCurricular, Docente, Turma
from dateutil.parser import parse


def carregar_docente(siape, componente):
    docente = get_docente_by_siape(siape)

    # Carregamento de Docente com Contrato de Professor Substituto
    if docente is None and siape is not None and siape != '':
        print("Adicionando Docente: " + siape + " - Substituto")
        docente = Docente(siape=siape, nome='SUBSTITUTO', sexo='X', formacao='Graduado/Mestre',
                          tipo_jornada_trabalho='Temporária',
                          vinculo='Contrato', categoria='PROFESSOR DO MAGISTERIO SUPERIOR',
                          classe_funcional='',
                          id_unidade_lotacao=componente.departamento.id_unidade,
                          lotacao=componente.departamento.nome, admissao=parse('2020/02/01'))
        docente.save()
    return docente


def carregar_turma(row):
    # TODO fazer o teste se a turma já existe aqui e retornar!

    siape = row[2] if row[2] != '' else None
    id_componente_curricular = row[5]

    if ComponenteCurricular.objects.filter(id_componente=id_componente_curricular).exists():
        cc = ComponenteCurricular.objects.get(id_componente=id_componente_curricular)

        docente = carregar_docente(siape=siape, componente=cc)

        curriculo = get_curriculo_by_cc(id_componente_curricular)

        id_turma = row[0]
        codigo_turma = row[1]
        matricula_docente_externo = row[3] if row[3] != '' else None
        observacao = row[4].strip()
        ch_dedicada_periodo = row[6] if row[6] != '' else None
        nivel_ensino = row[7]
        campus_turma = row[8]
        local = row[9]
        ano = row[10] if row[10] != '' else None
        periodo = row[11] if row[11] != '' else None
        data_inicio_str = row[12]
        data_inicio = parse(data_inicio_str)
        data_fim_str = row[13]
        data_fim = parse(data_fim_str)
        descricao_horario = row[14]
        total_solicitacoes = row[15] if row[15] != '' else None
        capacidade_aluno = row[16]
        tipo = row[17] if row[17] != '' else None
        distancia = row[18] if row[18] == 'true' else False
        data_consolidacao_str = row[19] if row[19] != '' else None
        data_consolidacao = data_consolidacao_str if data_consolidacao_str is None \
            else parse(data_consolidacao_str)
        agrupadora = row[20] if row[20] == 'true' else False
        id_turma_agrupadora = row[21] if row[21] != '' else None
        qtd_aulas_lancadas = row[22] if row[22] != '' else None
        situacao_turma = row[23]
        convenio = row[24]
        modalidade_participantes = row[25]

        if not Turma.objects.filter(id_turma=id_turma).exists():
            print("Adicionando Turma " + id_turma + " - " + codigo_turma + "- " + cc.codigo + " - " +
                  cc.nome + " - " + descricao_horario)
            turma = Turma(id_turma=id_turma, codigo_turma=codigo_turma, docente=docente,
                          matricula_docente_externo=matricula_docente_externo, observacao=observacao,
                          componente=cc, ch_dedicada_periodo=ch_dedicada_periodo,
                          nivel_ensino=nivel_ensino, campus_turma=campus_turma, local=local, ano=ano,
                          periodo=periodo, data_inicio=data_inicio, data_fim=data_fim,
                          descricao_horario=descricao_horario, total_solicitacoes=total_solicitacoes,
                          capacidade_aluno=capacidade_aluno, tipo=tipo, distancia=distancia,
                          data_consolidacao=data_consolidacao, agrupadora=agrupadora,
                          id_turma_agrupadora=id_turma_agrupadora, qtd_aulas_lancadas=qtd_aulas_lancadas,
                          situacao_turma=situacao_turma, convenio=convenio,
                          modalidade_participantes=modalidade_participantes)
            turma.save()
        else:
            print('.', end="")
