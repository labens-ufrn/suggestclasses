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
