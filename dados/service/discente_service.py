


from core.models import Discente


def atualizar_discente(
    matricula, nome_discente, sexo, ano_ingresso, periodo_ingresso, forma_ingresso,
    tipo_discente, status, sigla_nivel_ensino, nivel_ensino, id_curso, nome_curso,
    modalidade_educacao, id_unidade, nome_unidade, id_unidade_gestora, nome_unidade_gestora):

    discente = Discente.objects.get(matricula=matricula)

    atualizacoes = ''
    if discente.matricula == int(matricula):
        if not discente.nome_discente == nome_discente:
            atualizacoes += 'nome_discente = ' + discente.nome_discente + ' --> ' + nome_discente + ','
            discente.nome_discente = nome_discente

        if not discente.sexo == sexo:
            atualizacoes += 'sexo = ' + discente.sexo + ' --> ' + sexo + ','
            discente.sexo = sexo

        if not discente.ano_ingresso == ano_ingresso:
            atualizacoes += 'ano_ingresso = ' + discente.ano_ingresso + ' --> ' + ano_ingresso + ','
            discente.ano_ingresso = ano_ingresso

        if not discente.periodo_ingresso == periodo_ingresso:
            atualizacoes += 'periodo_ingresso = ' + discente.periodo_ingresso + ' --> ' + periodo_ingresso + ','
            discente.periodo_ingresso = periodo_ingresso

        if not discente.forma_ingresso == forma_ingresso:
            atualizacoes += 'forma_ingresso = ' + discente.forma_ingresso + ' --> ' + forma_ingresso + ','
            discente.forma_ingresso = forma_ingresso

        if not discente.tipo_discente == tipo_discente:
            atualizacoes += 'tipo_discente = ' + discente.tipo_discente + ' --> ' + tipo_discente + ','
            discente.tipo_discente = tipo_discente

        if not discente.status == status:
            atualizacoes += 'status = ' + discente.status + ' --> ' + status + ','
            discente.status = status

        if not discente.sigla_nivel_ensino == sigla_nivel_ensino:
            atualizacoes += 'sigla_nivel_ensino = ' + discente.sigla_nivel_ensino + ' --> ' + sigla_nivel_ensino + ','
            discente.sigla_nivel_ensino = sigla_nivel_ensino

        if not discente.nivel_ensino == nivel_ensino:
            atualizacoes += 'nivel_ensino = ' + discente.nivel_ensino + ' --> ' + nivel_ensino + ','
            discente.nivel_ensino = nivel_ensino

        if not discente.id_curso == id_curso:
            atualizacoes += 'id_curso = ' + discente.id_curso + ' --> ' + id_curso + ','
            discente.id_curso = id_curso

        if not discente.nome_curso == nome_curso:
            atualizacoes += 'nome_curso = ' + discente.nome_curso + ' --> ' + nome_curso + ','
            discente.nome_curso = nome_curso

        if not discente.modalidade_educacao == modalidade_educacao:
            atualizacoes += 'modalidade_educacao = ' + discente.modalidade_educacao + ' --> ' + modalidade_educacao + ','
            discente.modalidade_educacao = modalidade_educacao

        if not discente.id_unidade == id_unidade:
            atualizacoes += 'id_unidade = ' + discente.id_unidade + ' --> ' + id_unidade + ','
            discente.id_unidade = id_unidade

        if not discente.nome_unidade == nome_unidade:
            atualizacoes += 'nome_unidade = ' + discente.nome_unidade + ' --> ' + nome_unidade + ','
            discente.nome_unidade = nome_unidade

        if not discente.id_unidade_gestora == id_unidade_gestora:
            atualizacoes += 'id_unidade_gestora = ' + discente.id_unidade_gestora + ' --> ' + id_unidade_gestora + ','
            discente.id_unidade_gestora = id_unidade_gestora

        if not discente.nome_unidade_gestora == nome_unidade_gestora:
            atualizacoes += 'nome_unidade_gestora = ' + discente.nome_unidade_gestora + ' --> ' + nome_unidade_gestora + ','
            discente.nome_unidade_gestora = nome_unidade_gestora

        if len(atualizacoes) > 0:
            atualizacoes = atualizacoes[:-1]
            discente.save()
            print('*', end="")
        return discente, atualizacoes
    return None, None
