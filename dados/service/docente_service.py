from core.models import Docente


def atualizar_docente(
    siape, nome, sexo, formacao, tipo_jornada_trabalho, vinculo, categoria, \
    classe_funcional, id_unidade_lotacao, lotacao, admissao, depto):

    docente = Docente.objects.get(siape=siape)

    atualizacoes = ''
    if docente.siape == int(siape):
        if not docente.nome == nome:
            atualizacoes += 'nome = ' + docente.nome + ' --> ' + nome + ','
            docente.nome = nome

        if not docente.sexo == sexo:
            atualizacoes += 'sexo = ' + docente.sexo + ' --> ' + sexo + ','
            docente.sexo = sexo

        if not docente.formacao == formacao: 
            atualizacoes += 'formação = ' + docente.formacao + ' --> ' + formacao + ','
            docente.formacao = formacao

        if not docente.tipo_jornada_trabalho.strip() == tipo_jornada_trabalho.strip():
            atualizacoes += 'tipo jornada trabalho = ' + docente.tipo_jornada_trabalho.strip() + ' --> ' + tipo_jornada_trabalho.strip() + ','
            docente.tipo_jornada_trabalho = tipo_jornada_trabalho

        if not docente.vinculo == vinculo:
            atualizacoes += 'vínculo = ' + docente.vinculo + ' --> ' + vinculo + ','
            docente.vinculo = vinculo

        if not docente.categoria == categoria:
            atualizacoes += 'categoria = ' + docente.categoria + ' --> ' + categoria + ','
            docente.categoria = categoria

        if not docente.classe_funcional.strip() == classe_funcional.strip():
            atualizacoes += 'classe funcional = ' + docente.classe_funcional.strip() + ' --> ' + classe_funcional.strip() + ','
            docente.classe_funcional = classe_funcional

        if not docente.id_unidade_lotacao ==     int(id_unidade_lotacao):
            atualizacoes += 'unidade lotação = ' + str(docente.id_unidade_lotacao) + ' --> ' + id_unidade_lotacao + ','
            docente.id_unidade_lotacao = int(id_unidade_lotacao)

        if not docente.lotacao == lotacao:
            atualizacoes += 'lotação = ' + docente.lotacao + ' --> ' + lotacao + ','
            docente.lotacao = lotacao

        if not docente.admissao == admissao.date():
            atualizacoes += 'admissão = ' + str(docente.admissao) + ' --> ' + str(admissao) + ','
            docente.admissao = admissao.date()

        if not docente.departamento == depto:
            atualizacoes += 'depto = ' + docente.depto + ' --> ' + depto + ','
            docente.departamento = depto
        
        if len(atualizacoes) > 0:
            atualizacoes = atualizacoes[:-1]
            docente.save()
            print('*', end="")
        return docente, atualizacoes
    return None, None