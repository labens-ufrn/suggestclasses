


from core.models import ComponenteCurricular


def atualizar_componente_curricular(
    id_componente, tipo_componente, codigo_componente, nivel_componente, nome_componente,
    ch_teorica, ch_pratica, ch_estagio, ch_total, ch_dedicada_docente, ch_ead, cr_max_ead,
    equivalencia, pre_requisito, co_requisito, ementa, modalidade, depto):

    cc = ComponenteCurricular.objects.get(id_componente=id_componente)

    atualizacoes = ''
    if cc.id_componente == int(id_componente):
        if not cc.tipo == tipo_componente:
            atualizacoes += 'tipo = ' + cc.tipo + ' --> ' + tipo_componente + ','
            cc.tipo = tipo_componente
            print('*', end="")
        if not cc.codigo == codigo_componente:
            atualizacoes += 'codigo = ' + cc.codigo + ' --> ' + codigo_componente + ','
            cc.codigo = codigo_componente
            print('*', end="")
        if not cc.nivel == nivel_componente:
            atualizacoes += 'nivel = ' + cc.nivel + ' --> ' + nivel_componente + ','
            cc.nivel = nivel_componente
            print('*', end="")
        if not cc.nome == nome_componente:
            atualizacoes += 'nome = ' + cc.nome + ' --> ' + nome_componente + ','
            cc.nome = nome_componente
            print('*', end="")
        if not cc.ch_teorica == int(ch_teorica):
            atualizacoes += 'ch_teorica = ' + str(cc.ch_teorica) + ' --> ' + ch_teorica + ','
            cc.ch_teorica = int(ch_teorica)
            print('*', end="")
        if not cc.ch_pratica == int(ch_pratica):
            atualizacoes += 'ch_pratica = ' + str(cc.ch_pratica) + ' --> ' + ch_pratica + ','
            cc.ch_pratica = int(ch_pratica)
            print('*', end="")
        if not cc.ch_estagio == int(ch_estagio):
            atualizacoes += 'ch_estagio = ' + str(cc.ch_estagio) + ' --> ' + ch_estagio + ','
            cc.ch_estagio = int(ch_estagio)
            print('*', end="")
        if not cc.ch_total == int(ch_total):
            atualizacoes += 'ch_total = ' + str(cc.ch_total) + ' --> ' + ch_total + ','
            cc.ch_total = int(ch_total)
            print('*', end="")
        if not cc.ch_docente == int(ch_dedicada_docente):
            atualizacoes += 'ch_docente = ' + str(cc.ch_docente) + ' --> ' + ch_dedicada_docente + ','
            cc.ch_docente = int(ch_dedicada_docente)
            print('*', end="")
        if not cc.ch_ead == int(ch_ead):
            atualizacoes += 'ch_ead = ' + str(cc.ch_ead) + ' --> ' + ch_ead + ','
            cc.ch_ead = int(ch_ead)
            print('*', end="")
        if not cc.cr_max_ead == int(cr_max_ead):
            atualizacoes += 'cr_max_ead = ' + str(cc.cr_max_ead) + ' --> ' + cr_max_ead + ','
            cc.cr_max_ead = int(cr_max_ead)
            print('*', end="")
        if not cc.equivalencia == equivalencia:
            atualizacoes += 'equivalencia = ' + cc.equivalencia + ' --> ' + equivalencia + ','
            cc.equivalencia = equivalencia
            print('*', end="")
        if not cc.requisito == pre_requisito:
            atualizacoes += 'requisito = ' + cc.requisito + ' --> ' + pre_requisito + ','
            cc.requisito = pre_requisito
            print('*', end="")
        if not cc.corequisito == co_requisito:
            atualizacoes += 'corequisito = ' + cc.corequisito + ' --> ' + co_requisito + ','
            cc.corequisito = co_requisito
            print('*', end="")
        if not cc.ementa == ementa:
            atualizacoes += 'ementa = ' + cc.ementa + ' --> ' + ementa + ','
            cc.ementa = ementa
            print('*', end="")
        if not cc.modalidade == modalidade:
            atualizacoes += 'modalidade = ' + cc.modalidade + ' --> ' + modalidade + ','
            cc.modalidade = modalidade
            print('*', end="")

        if len(atualizacoes) > 0:
            atualizacoes = atualizacoes[:-1]
            cc.save()
        return cc, atualizacoes
    return None, None
