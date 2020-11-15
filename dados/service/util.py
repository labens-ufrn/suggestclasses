from datetime import datetime


def gravar_arquivo(nome_arquivo, lista_modificacoes):

    data_e_hora_atuais = datetime.now()
    arquivo = open("atualizados/" + nome_arquivo + "-" + str(data_e_hora_atuais) + ".txt", "a")
    for modificacao in lista_modificacoes:
    # \n is placed to indicate EOL (End of Line)
        arquivo.write(modificacao + '\n')
    arquivo.close()