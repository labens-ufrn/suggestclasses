from core.models import EstruturaCurricular

SETA = ' --> '
STATUS_ATIVA = '1'
STATUS_INATIVA = '2'

def atualizar_estrutura(ec_nova):

    ec_antiga = EstruturaCurricular.objects.get(id_curriculo=ec_nova.id_curriculo)

    atualizacoes = ''
    if ec_antiga:
        if not ec_antiga.codigo == ec_nova.codigo:
            atualizacoes += 'código = ' + ec_antiga.codigo + SETA + ec_nova.codigo + ','
            ec_antiga.codigo = ec_nova.codigo

        if not ec_antiga.nome == ec_nova.nome:
            atualizacoes += 'nome = ' + ec_antiga.nome + SETA + ec_nova.nome + ','
            ec_antiga.nome = ec_nova.nome

        if not ec_antiga.observacao == ec_nova.observacao:
            atualizacoes += 'observacao = ' + ec_antiga.observacao + SETA + ec_nova.observacao + ','
            ec_antiga.observacao = ec_nova.observacao

        if not ec_antiga.status == STATUS_ATIVA:
            atualizacoes += 'Status = ' + str(ec_antiga.status) + SETA + 'ATIVA' + ','
            ec_antiga.status = STATUS_ATIVA

        if len(atualizacoes) > 0:
            atualizacoes = atualizacoes[:-1]
            ec_antiga.save()
            print('*', end="")
        return ec_antiga, atualizacoes
    return None, None
