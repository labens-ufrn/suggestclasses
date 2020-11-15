


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
            print('*', end="")
        if not discente.sexo == sexo:
            atualizacoes += 'sexo = ' + discente.sexo + ' --> ' + sexo + ','
            discente.sexo = sexo
            print('*', end="")
        if not discente.ano_ingresso == ano_ingresso:
            atualizacoes += 'ano_ingresso = ' + discente.ano_ingresso + ' --> ' + ano_ingresso + ','
            discente.ano_ingresso = ano_ingresso
            print('*', end="")
        if not discente.periodo_ingresso == periodo_ingresso:
            atualizacoes += 'periodo_ingresso = ' + discente.periodo_ingresso + ' --> ' + periodo_ingresso + ','
            discente.periodo_ingresso = periodo_ingresso
            print('*', end="")
        if not discente.forma_ingresso == forma_ingresso:
            atualizacoes += 'forma_ingresso = ' + discente.forma_ingresso + ' --> ' + forma_ingresso + ','
            discente.forma_ingresso = forma_ingresso
            print('*', end="")
        if not discente.tipo_discente == tipo_discente:
            atualizacoes += 'tipo_discente = ' + discente.tipo_discente + ' --> ' + tipo_discente + ','
            discente.tipo_discente = tipo_discente
            print('*', end="")
        if not discente.status == status:
            atualizacoes += 'status = ' + discente.status + ' --> ' + status + ','
            discente.status = status
            print('*', end="")
        if not discente.sigla_nivel_ensino == sigla_nivel_ensino:
            atualizacoes += 'sigla_nivel_ensino = ' + discente.sigla_nivel_ensino + ' --> ' + sigla_nivel_ensino + ','
            discente.sigla_nivel_ensino = sigla_nivel_ensino
            print('*', end="")
        if not discente.nivel_ensino == nivel_ensino:
            atualizacoes += 'nivel_ensino = ' + discente.nivel_ensino + ' --> ' + nivel_ensino + ','
            discente.nivel_ensino = nivel_ensino
            print('*', end="")
        if not discente.id_curso == id_curso:
            atualizacoes += 'id_curso = ' + discente.id_curso + ' --> ' + id_curso + ','
            discente.id_curso = id_curso
            print('*', end="")
        if not discente.nome_curso == nome_curso:
            atualizacoes += 'nome_curso = ' + discente.nome_curso + ' --> ' + nome_curso + ','
            discente.nome_curso = nome_curso
            print('*', end="")
        if not discente.modalidade_educacao == modalidade_educacao:
            atualizacoes += 'modalidade_educacao = ' + discente.modalidade_educacao + ' --> ' + modalidade_educacao + ','
            discente.modalidade_educacao = modalidade_educacao
            print('*', end="")
        if not discente.id_unidade == id_unidade:
            atualizacoes += 'id_unidade = ' + discente.id_unidade + ' --> ' + id_unidade + ','
            discente.id_unidade = id_unidade
            print('*', end="")
        if not discente.nome_unidade == nome_unidade:
            atualizacoes += 'nome_unidade = ' + discente.nome_unidade + ' --> ' + nome_unidade + ','
            discente.nome_unidade = nome_unidade
            print('*', end="")
        if not discente.id_unidade_gestora == id_unidade_gestora:
            atualizacoes += 'id_unidade_gestora = ' + discente.id_unidade_gestora + ' --> ' + id_unidade_gestora + ','
            discente.id_unidade_gestora = id_unidade_gestora
            print('*', end="")
        if not discente.nome_unidade_gestora == nome_unidade_gestora:
            atualizacoes += 'nome_unidade_gestora = ' + discente.nome_unidade_gestora + ' --> ' + nome_unidade_gestora + ','
            discente.nome_unidade_gestora = nome_unidade_gestora
            print('*', end="")

        if len(atualizacoes) > 0:
            atualizacoes = atualizacoes[:-1]
            # discente.save()
        return discente, atualizacoes
    return None, None