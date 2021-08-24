from core.models import Centro, Departamento


def atualizar_unidade(id_dep, codigo_dep, nome_dep, sigla_dep, municipio, id_unidade_responsavel):

    departamento = Departamento.objects.get(id_unidade=id_dep)

    atualizacoes = ''
    if departamento.id_unidade == int(id_dep):
        if not departamento.nome == nome_dep:
            atualizacoes += 'nome = ' + departamento.nome + ' --> ' + nome_dep + ','
            departamento.nome = nome_dep

        if not departamento.sigla == sigla_dep:
            atualizacoes += 'sigla = ' + departamento.sigla + ' --> ' + sigla_dep + ','
            departamento.sigla = sigla_dep

        if not departamento.endereco == municipio:
            atualizacoes += 'formação = ' + departamento.endereco + ' --> ' + municipio + ','
            departamento.endereco = municipio

        unidade_responsavel = Centro.objects.get(id_unidade=id_unidade_responsavel)

        if not departamento.centro == unidade_responsavel:
            atualizacoes += 'centro = ' + departamento.centro.sigla + ' --> ' + unidade_responsavel.sigla + ','
            departamento.centro = unidade_responsavel

        if len(atualizacoes) > 0:
            atualizacoes = atualizacoes[:-1]
            departamento.save()
            print('*', end="")
        return departamento, atualizacoes
    return None, None
