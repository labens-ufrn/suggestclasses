from core.models import Curso

SETA = ' --> '

def atualizar_curso(
    id_curso, nome_curso, docente, nivel_ensino,
    grau_academico, modalidade_educacao, turno, ceres):

    curso = Curso.objects.get(codigo=id_curso)

    atualizacoes = ''
    if curso.codigo == int(id_curso):
        if not curso.nome == nome_curso:
            atualizacoes += 'nome = ' + curso.nome + SETA + nome_curso + ','
            curso.nome = nome_curso

        if not curso.coordenador == docente:
            atualizacoes += 'coordenador = ' + str(curso.coordenador) + SETA + str(docente) + ','
            curso.coordenador = docente

        if not curso.nivel == nivel_ensino:
            atualizacoes += 'nivel_ensino = ' + curso.nivel + SETA + nivel_ensino + ','
            curso.nivel = nivel_ensino

        if not curso.grau == grau_academico:
            atualizacoes += 'grau acadêmico = ' + curso.grau + SETA + grau_academico + ','
            curso.tipo_jornada_trabalho = grau_academico

        if not curso.modalidade == modalidade_educacao:
            atualizacoes += 'modalidade educação = ' + curso.modalidade + SETA + modalidade_educacao + ','
            curso.modalidade = modalidade_educacao

        if not curso.turno == turno:
            atualizacoes += 'turno = ' + curso.turno + SETA + turno + ','
            curso.turno = turno

        if not curso.centro == ceres:
            atualizacoes += 'centro = ' + curso.centro + ' --> ' + ceres + ','
            curso.centro = ceres

        if len(atualizacoes) > 0:
            atualizacoes = atualizacoes[:-1]
            curso.save()
            print('*', end="")
        return curso, atualizacoes
    return None, None
