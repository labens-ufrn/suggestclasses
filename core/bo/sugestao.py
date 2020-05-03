from django.contrib import messages
from core.models import SolicitacaoTurma, SugestaoTurma


def solicitacao_incluir(usuario, turma_pk):
    discente = usuario.discente
    turma = SugestaoTurma.objects.get(pk=turma_pk)

    solicitacao, created = SolicitacaoTurma.objects.get_or_create(
        usuario=usuario, solicitador=discente, turma=turma)

    return solicitacao, created

    # TODO Atualizar total de solicitações na Turma?? É necessário??
    # sugestao_turma.total_solicitacoes = 0


def solicitacao_existe(discente, turma):
    return SolicitacaoTurma.objects.filter(solicitador=discente, turma=turma).exists()


def solicitacao_verificar_choques(turma, discente):
    choques_horarios = []
    choques_componentes = set()
    horarios_list = turma.horarios.all()
    for horario in horarios_list:
        solicitacoes = SolicitacaoTurma.objects.filter(solicitador=discente)
        if solicitacoes:
            for s in solicitacoes:
                st = s.turma
                if st.codigo_turma == turma.codigo_turma and \
                   st.componente == turma.componente:
                    break
                if horario in st.horarios.all():
                    choques_componentes.add(str(st.componente.codigo) + ' - ' + st.componente.nome)
                    choques_horarios.append(horario.dia + horario.turno + horario.ordem)

    if choques_horarios:
        return choques_componentes, choques_horarios, True
    return None, None, False

