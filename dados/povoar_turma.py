import os
import csv
import django
django.setup()
from core.bo.curriculo import get_curriculo_by_cc
from core.bo.docente import get_docente_by_siape
from core.bo.turma import converte_desc_horario
from core.models import ComponenteCurricular, Docente, Turma
from dateutil.parser import parse
from mysite.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')


def main():
    print("Povoar Turmas da UFRN!")
    os.chdir(DADOS_PATH)
    criar_turmas()


def criar_turmas():
    print("Criando Turmas 2019.1, 2019.2 e 2020.1 para os Cursos do CERES ...!")

    criar_turmas_semestre('turmas-2019.1.csv')
    criar_turmas_semestre('turmas-2019.2.csv')
    criar_turmas_semestre('turmas-2020.1.csv')


def criar_turmas_semestre(turmas_csv):
    print("Criando Turmas: " + turmas_csv + " para os Cursos do CERES ...!")

    with open(turmas_csv) as csvfile:
        turmas = csv.reader(csvfile, delimiter=';')
        next(turmas)  # skip header

        for row in turmas:
            carregar_turma(row)
        print()


def carregar_turma(row):
    # TODO fazer o teste se a turma já existe aqui e retornar!

    id_componente_curricular = row[5]

    if ComponenteCurricular.objects.filter(id_componente=id_componente_curricular).exists():
        id_turma = row[0]
        codigo_turma = row[1]
        siape = row[2] if row[2] != '' else None
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

        if id_turma == 57640954:
            print(descricao_horario)

        cc = ComponenteCurricular.objects.get(id_componente=id_componente_curricular)
        docente = carregar_docente_substituto(siape=siape, componente=cc)

        curriculo = get_curriculo_by_cc(id_componente_curricular)

        if Turma.objects.filter(id_turma=id_turma).exists():
            turma = Turma.objects.get(id_turma=id_turma)
            print(str(docente) + ' ' + ch_dedicada_periodo)
            # adicionar_vinculo_docente(turma, docente, carga_horaria, horarios_docente)
            print('-', end="")
        else:
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
            horarios_list = converte_desc_horario(descricao_horario)
            turma.horarios.set(horarios_list)
            print('.', end="")


def carregar_docente_substituto(siape, componente):
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


if __name__ == "__main__":
    main()
