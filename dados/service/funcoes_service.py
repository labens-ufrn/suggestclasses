from core.models import FuncaoGratificada


def atualizar_funcao(
    siape, nome, situacao_servidor, id_unidade, lotacao, sigla, inicio, fim, 
    id_unidade_designacao, unidade_designacao, atividade, observacoes):

    funcao = FuncaoGratificada.objects.get(
                siape=siape, id_unidade=id_unidade, inicio=inicio, atividade=atividade)

    atualizacoes = ''
    if funcao.siape == int(siape) and funcao.id_unidade == int(id_unidade) and \
       funcao.inicio == inicio.date() and funcao.atividade == atividade:

        if not funcao.nome == nome:
            atualizacoes += 'nome = ' + funcao.nome + ' --> ' + nome + ','
            funcao.nome = nome

        if not funcao.situacao_servidor == situacao_servidor:
            atualizacoes += 'situacao_servidor = ' + funcao.situacao_servidor + ' --> ' + situacao_servidor + ','
            funcao.situacao_servidor = situacao_servidor

        if not funcao.id_unidade == int(id_unidade): 
            atualizacoes += 'id_unidade = ' + funcao.id_unidade + ' --> ' + id_unidade + ','
            funcao.id_unidade = int(id_unidade)

        if not funcao.lotacao == lotacao:
            atualizacoes += 'lotação = ' + funcao.lotacao + ' --> ' + lotacao + ','
            funcao.lotacao = lotacao

        if not funcao.sigla == sigla:
            atualizacoes += 'sigla = ' + funcao.sigla + ' --> ' + sigla + ','
            funcao.sigla = sigla

        if not funcao.inicio == inicio.date():
            atualizacoes += 'inicio = ' + str(funcao.inicio) + ' --> ' + str(inicio) + ','
            funcao.inicio = inicio.date()

        if fim is not None and not funcao.fim == fim.date():
            atualizacoes += 'fim = ' + str(funcao.fim) + ' --> ' + str(fim) + ','
            funcao.fim = fim.date()

        if not funcao.id_unidade_designacao == int(id_unidade_designacao):
            atualizacoes += 'id_unidade_designacao = ' + funcao.id_unidade_designacao + ' --> ' + id_unidade_designacao + ','
            funcao.id_unidade_designacao = int(id_unidade_designacao)

        if not funcao.unidade_designacao == unidade_designacao:
            atualizacoes += 'unidade_designacao = ' + funcao.unidade_designacao + ' --> ' + unidade_designacao + ','
            funcao.unidade_designacao = unidade_designacao

        if not funcao.atividade == atividade:
            atualizacoes += 'atividade = ' + funcao.atividade + ' --> ' + atividade + ','
            funcao.atividade = atividade

        if not funcao.observacoes == observacoes:
            atualizacoes += 'observacoes = ' + funcao.observacoes + ' --> ' + observacoes + ','
            funcao.observacoes = observacoes
        
        if len(atualizacoes) > 0:
            atualizacoes = atualizacoes[:-1]
            funcao.save()
            print('*', end="")
        return funcao, atualizacoes
    return None, None