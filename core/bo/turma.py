import re

from core.bo.sevices import get_oc_by_semestre
from core.config.config import get_config
from core.models import Turma, Horario, SugestaoTurma


def get_turmas(estrutura, semestre, ano, periodo):
    org_curricular = get_oc_by_semestre(estrutura, semestre)

    turmas_result = []
    for oc in org_curricular:
        # Classe Turma Estendida para guardar informações de Organização Curricular ( tipo_vinculo, semestre, curso)
        turmas = Turma.objects.filter(componente=oc.componente, ano=ano, periodo=periodo)

        for t in turmas:
            turma_estendida = TurmaEstendida(t, oc.tipo_vinculo, oc.semestre, estrutura.curso)
            turmas_result.append(turma_estendida)

    return turmas_result


def get_sugestao_turmas(estrutura, semestre, ano, periodo):
    """
    Retorna a lista de Sugestões de Turmas de um semestre de um Curso no ano-período definido.
    :param estrutura: A Estrutura Curricular do Curso. # TODO Mudar para passar apenas o curso.
    :param semestre: O semestre que as turmas são ofertadas (1, 2, 3, 4, 5, 6, 7, 8, 0).
    :param ano: Ano do calendário acadêmico.
    :param periodo: Periodo do calendário acadêmico: 1º ou 2º.
    :return: Uma lista de @SugestaoTurma para o curso naquele semestre.
    """
    sugestoes_turmas = list(
        SugestaoTurma.objects.filter(curso=estrutura.curso, semestre=semestre, ano=ano, periodo=periodo))

    return sugestoes_turmas


def get_turmas_por_horario(turmas, dia, turno, ordem):
    turmas_horario = []
    horario = Horario.objects.get(dia=dia, turno=turno, ordem=ordem)
    for t in turmas:
        horarios_turma = list(t.horarios.all())
        if not horarios_turma:
            print('Turma sem Horário: ' + t.componente.nome)
        if horario in horarios_turma:
            turmas_horario.append(t)
    return turmas_horario


def converte_desc_horario(descricao_horario):
    horarios_list = []
    # Trata descricao_horario vazia e turno None.
    if descricao_horario == '' or descricao_horario is None:
        return horarios_list

    horarios_split = descricao_horario.split()

    for hs in horarios_split:
        hs_tratado = verificar_formato(hs)
        if hs_tratado is not None:
            turno = get_turno(hs)
            horarios = converte_horario_simples(hs, turno)
            horarios_list.extend(horarios)

    return horarios_list


def verificar_formato(horario_simples):
    hs_tratado = None

    p = re.compile('[1-7]+[MTNmtn][1-6]+')
    m = p.match(horario_simples)

    if m is not None:
        hs_tratado = m.group()

    return hs_tratado


def converte_horario_simples(horario, turno):
    horarios_list = []
    horario_split = horario.split(turno)
    dias = horario_split[0]
    ordens = horario_split[1]
    for d in dias:
        for o in ordens:
            horario = Horario.objects.get(dia=str(d), turno=turno, ordem=str(o))
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


def carrega_turmas(estrutura, semestres, ano_periodo):
    semestres = atualiza_semestres(semestres)
    ano_periodo = atualiza_ano_periodo(ano_periodo)
    ano = get_ano(ano_periodo)
    periodo = get_periodo(ano_periodo)

    turmas = []
    for s in semestres:
        ts = get_turmas(estrutura, s, ano, periodo)
        turmas.extend(ts)
    return turmas


def atualiza_semestres(semestres):
    if semestres is None or semestres.__contains__('100') or semestres == []:
        semestres = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    return semestres


def atualiza_ano_periodo(ano_periodo):
    if ano_periodo is None or ano_periodo == []:
        config = get_config()
        ano_periodo = [config.get('PeriodoAtual', 'ano_periodo')]
    return ano_periodo


def teste_vazio(ano_periodo):
    return ano_periodo is None or ano_periodo == [] or ano_periodo[0] == ''


def get_ano(ano_periodo):
    if not teste_vazio(ano_periodo):
        ano = ano_periodo[0].split('.')[0]
        return ano
    return None


def get_periodo(ano_periodo):
    if not teste_vazio(ano_periodo):
        p = ano_periodo[0].split('.')[1]
        return p
    return None


def carrega_sugestao_turmas(estrutura, semestres, ano, periodo):
    turmas = []
    for s in semestres:
        ts = get_sugestao_turmas(estrutura, s, ano, periodo)
        turmas.extend(ts)
    return turmas


def carrega_turmas_horario(turmas):
    """
    Carrega uma lista com 16 posições representando os 16 períodos de 50 min de aulas em todos os turnos.
    Cada posição contém outra lista de 5 posições representando os dias da semana.
    :param turmas: Uma lista de Turmas ou Sugestões de Turma.
    :return: Uma lista bidimensional representando a grade de horários com a lista de turmas
    em cada horário.
    """
    tt = []
    tt.extend(carrega_horario_turmas_por_turno(turmas, 'M'))
    tt.extend(carrega_horario_turmas_por_turno(turmas, 'T'))
    tt.extend(carrega_horario_turmas_por_turno(turmas, 'N'))
    return tt


def carrega_horario_turmas_por_turno(turmas, turno):
    """
    Carrega uma lista com 16 posições representando os 16 períodos de 50 min de aulas para um turno.
    Cada posição contém outra lista de 5 posições representando os dias da semana.
    :param turmas: Uma lista de Turmas ou Sugestões de Turma.
    :param turno: Turno selecionado entre as opções M, T e N.
    :return: Uma lista bidimensional representando a grade de horários com a lista de turmas
    em cada horário.
    """
    tt = []
    n = 7
    if turno == 'N':
        n = 5

    for i in range(1, n):
        horarios = Horario.objects.filter(turno=turno, ordem=i).order_by('dia')
        turmas_horario = []
        for h in horarios:
            turmas_por_horario = get_turmas_por_horario(turmas=turmas, dia=h.dia, turno=turno, ordem=i)
            th = TurmaHorario(h, turmas_por_horario)
            turmas_horario.append(th)
        tt.append(turmas_horario)
    return tt


def carrega_sugestao_horario(curso, ano, periodo):
    """
    Carrega uma lista com 16 posições representando os 16 períodos de 50 min de aulas em todos os turnos.
    Cada posição contém outra lista de 5 posições representando os dias da semana.
    :param turmas: Uma lista de Turmas ou Sugestões de Turma.
    :return: Uma lista bidimensional representando a grade de horários com a lista de turmas
    em cada horário.
    """
    tt = []
    tt.extend(carrega_horario_sugestao_por_turno(curso, 'M', ano, periodo))
    tt.extend(carrega_horario_sugestao_por_turno(curso, 'T', ano, periodo))
    tt.extend(carrega_horario_sugestao_por_turno(curso, 'N', ano, periodo))
    return tt


def carrega_horario_sugestao_por_turno(curso, turno, ano, periodo):
    """
    Carrega uma lista com 16 posições representando os 16 horários de aula de 50 min de aulas para um turno.
    Cada posição contém outra lista de 5 posições representando os dias da semana.
    :param curso: Curso de interesse para carregar turmas.
    :param ano: Ano do calendário acadêmico das turmas.
    :param periodo: Período do calendário acadêmico das turmas.
    :param turno: Turno selecionado entre as opções M, T e N.
    :return: Uma lista bidimensional representando a grade de horários com a lista de turmas
    em cada horário.
    """
    tt = []
    n = 7
    if turno == 'N':
        n = 5

    for i in range(1, n):
        horarios = Horario.objects.filter(turno=turno, ordem=i).order_by('dia')
        turmas_horario = []
        for h in horarios:
            turmas_por_horario = get_sugestoes_por_horario(h, curso, ano, periodo)
            th = TurmaHorario(h, turmas_por_horario)
            turmas_horario.append(th)
        tt.append(turmas_horario)
    return tt


def get_sugestoes_por_horario(horario, curso, ano, periodo):
    turmas_por_horario = list(horario.sugestoes.all().filter(curso=curso, ano=ano, periodo=periodo))
    return turmas_por_horario


class TurmaHorario(object):

    def __init__(self, horario, turmas):
        # salva os dados  que foram passados
        self.turmas = turmas
        self.horario = horario

    def __str__(self):
        return self.horario.__str__() + self.turmas.__str__()


class TurmaEstendida(Turma):

    def __init__(self, turma, tipo_vinculo, semestre, curso):
        super(TurmaEstendida, self)\
            .__init__(id_turma=turma.id_turma, codigo_turma=turma.codigo_turma, docente=turma.docente,
                      matricula_docente_externo=turma.matricula_docente_externo, observacao=turma.observacao,
                      componente=turma.componente, ch_dedicada_periodo=turma.ch_dedicada_periodo,
                      nivel_ensino=turma.nivel_ensino, campus_turma=turma.campus_turma, local=turma.local,
                      ano=turma.ano, periodo=turma.periodo, data_inicio=turma.data_inicio, data_fim=turma.data_fim,
                      descricao_horario=turma.descricao_horario, total_solicitacoes=turma.total_solicitacoes,
                      capacidade_aluno=turma.capacidade_aluno, tipo=turma.tipo, distancia=turma.distancia,
                      data_consolidacao=turma.data_consolidacao, agrupadora=turma.agrupadora,
                      id_turma_agrupadora=turma.id_turma_agrupadora, qtd_aulas_lancadas=turma.qtd_aulas_lancadas,
                      situacao_turma=turma.situacao_turma, convenio=turma.convenio,
                      modalidade_participantes=turma.modalidade_participantes)
        self.pk = turma.pk
        self.tipo_vinculo = tipo_vinculo
        self.semestre = semestre
        self.curso = curso


# class SugestaoTurmaEstendida(SugestaoTurma):
#
#     def __init__(self, turma, tipo_vinculo, semestre, curso):
#         super(SugestaoTurmaEstendida, self)\
#             .__init__(codigo_turma=turma.codigo_turma, docente=turma.docente,
#                       matricula_docente_externo=turma.matricula_docente_externo,
#                       componente=turma.componente, campus_turma=turma.campus_turma, local=turma.local,
#                       ano=turma.ano, periodo=turma.periodo, descricao_horario=turma.descricao_horario,
#                       total_solicitacoes=turma.total_solicitacoes,
#                       capacidade_aluno=turma.capacidade_aluno, tipo=turma.tipo, criador=turma.criador)
#         self.pk = turma.pk
#         print(self.horarios.all())
#         self.horarios.clear()
#         print(self.horarios.all())
#         horario_list = turma.horarios.all()
#         self.horarios.set(horario_list)
#         self.tipo_vinculo = tipo_vinculo
#         self.semestre = semestre
#         self.curso = curso
