from core.models import Centro, Discente


def carregar_discentes(row):
    id_unidade = row[13] if row[13] != '' else None

    # Carregamento apenas de alunos do CERES.
    if Centro.objects.filter(id_unidade=id_unidade).exists():
        matricula = row[0]
        nome_discente = row[1]
        sexo = row[2]
        ano_ingresso = row[3]
        periodo_ingresso = row[4]
        forma_ingresso = row[5]
        tipo_discente = row[6]
        status = row[7]
        sigla_nivel_ensino = row[8]
        nivel_ensino = row[9]
        id_curso = row[10]
        nome_curso = row[11]
        modalidade_educacao = row[12]
        id_unidade = row[13]
        nome_unidade = row[14]
        id_unidade_gestora = row[15]
        nome_unidade_gestora = row[16]

        if not Discente.objects.filter(matricula=matricula).exists():
            print("Adicionando Discente " + matricula + " - " + nome_discente + "- " + nome_curso)
            discente = Discente(matricula=matricula, nome_discente=nome_discente, sexo=sexo,
                                ano_ingresso=ano_ingresso, periodo_ingresso=periodo_ingresso,
                                forma_ingresso=forma_ingresso, tipo_discente=tipo_discente, status=status,
                                sigla_nivel_ensino=sigla_nivel_ensino, nivel_ensino=nivel_ensino,
                                id_curso=id_curso, nome_curso=nome_curso, modalidade_educacao=modalidade_educacao,
                                id_unidade=id_unidade, nome_unidade=nome_unidade,
                                id_unidade_gestora=id_unidade_gestora, nome_unidade_gestora=nome_unidade_gestora)
            discente.save()
        else:
            print('.', end="")
