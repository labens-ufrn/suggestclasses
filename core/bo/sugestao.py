from django.contrib import messages

from core.bo.periodos import get_periodo_planejado
from core.models import SolicitacaoTurma, SugestaoTurma


def solicitacao_incluir(discente, sugestao_turma):
    """
    Inclui uma Solicitação de interesse do Discente na Sugestão de Turma.
    :param discente: Um objeto da classe @Discente
    :param sugestao_turma: Um objeto da classe @SugestaoTurma
    :return: Um objeto da classe @SolicitacaoTurma e um booleano informando se a Solicitação foi criada.
    """
    usuario = discente.usuario

    solicitacao, created = SolicitacaoTurma.objects.get_or_create(
        usuario=usuario, solicitador=discente, turma=sugestao_turma)

    return solicitacao, created


def solicitacao_existe(discente, sugestao_turma):
    """
    Verifica se existe uma Solicitação de interesse do Discente na Sugestão de Turma.
    :param discente: Um objeto da classe @Discente
    :param sugestao_turma: Um objeto da classe @SugestaoTurma
    :return: True se a Solicitação de interesse existir.
    """
    return SolicitacaoTurma.objects.filter(solicitador=discente, turma=sugestao_turma).exists()


def solicitacao_verificar_choques(discente, sugestao_turma):
    """
    Verifica se existe choque de horários do discente com a Sugestão de Turma.
    :param discente: Um objeto da classe @Discente
    :param sugestao_turma: Um objeto da classe @SugestaoTurma
    :return: Um conjunto de componentes em Choque, Um conjunto de horários em Choque e
     True se existir algum choque de horários com a Sugestão de Turma.
    """
    # periodo_letivo = get_periodo_planejado()
    choques_horarios = []
    choques_componentes = set()
    horarios_list = sugestao_turma.horarios.all()
    solicitacoes = SolicitacaoTurma.objects.filter(
        solicitador=discente, turma__ano=sugestao_turma.ano, turma__periodo=sugestao_turma.periodo)
    for horario in horarios_list:
        for s in solicitacoes:
            st = s.turma
            if eh_mesma_turma(st, sugestao_turma):
                break
            if horario in st.horarios.all():
                choques_componentes.add(str(st.componente.codigo) + ' - ' + st.componente.nome)
                choques_horarios.append(horario.dia + horario.turno + horario.ordem)

    if choques_horarios:
        return choques_componentes, choques_horarios, True
    return None, None, False


def eh_mesma_turma(sugestao1, sugestao2):
    """
    Verifica se o código e o componente das Sugestões de Turma são os mesmos.
    :param sugestao1: Um objeto da classe @SugestaoTurma
    :param sugestao2: Um objeto da classe @SugestaoTurma
    :return: True se as Sugestões tiverem mesmo código e mesmo componente.
    """
    return sugestao1.codigo_turma == sugestao2.codigo_turma and sugestao1.componente == sugestao2.componente
