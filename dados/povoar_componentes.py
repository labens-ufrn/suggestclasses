from datetime import datetime
import os
import csv
import django
from dateutil.parser import parse
django.setup()

from core.models import Departamento, ComponenteCurricular
from dados.service.componente_service import atualizar_componente_curricular
from suggestclasses.settings import BASE_DIR

DADOS_PATH = os.path.join(BASE_DIR, 'dados')

componentes_atualizados_set = set()


def main():
    os.chdir(DADOS_PATH)
    carregar_componentes()


def carregar_componentes():
    print("\nCriando Componentes para os Departamentos do CERES ...!")

    with open('componentes-curriculares-presenciais.csv') as csvfile:
        componentes_ceres = csv.reader(csvfile, delimiter=';')
        next(componentes_ceres)  # skip header

        for row in componentes_ceres:
            carregar_componente(row)
        print()
    
    data_e_hora_atuais = datetime.now()
    componentes_atualizados = open("componentes_atualizados " + str(data_e_hora_atuais) + ".txt", "a")
    for cc_modificados in componentes_atualizados_set:
        # \n is placed to indicate EOL (End of Line)
        componentes_atualizados.write(cc_modificados + '\n')
    componentes_atualizados.close()


def carregar_componente(row):
    unidade_responsavel = row[5].strip()

    if Departamento.objects.filter(nome=unidade_responsavel).exists():
        depto = Departamento.objects.get(nome=unidade_responsavel)

        id_componente = row[0]
        tipo_componente = row[1]
        codigo_componente = row[2]

        nivel_componente = row[3]
        nome_componente = row[4]

        ch_teorico = row[6]
        ch_pratico = row[7]
        ch_estagio = row[8]
        ch_total = row[9]
        ch_dedicada_docente = row[10]
        ch_ead = row[11]
        cr_max_ead = row[12]
        equivalencia = row[16]
        pre_requisito = row[17]
        co_requisito = row[18]
        ementa = row[19]
        bibliografia = row[20]
        objetivos = row[21]
        conteudo = row[22]
        competencias_habilidades = row[23]
        referencias = row[24]
        ano_programa = row[25]
        periodo_programa = row[26]
        modalidade = row[27]
        curso_componente = row[28]

        if not ComponenteCurricular.objects.filter(id_componente=id_componente).exists():
            print("Adicionando Componente " + id_componente + " - " + codigo_componente + " - "
                    + nome_componente)
            cc = ComponenteCurricular(id_componente=id_componente, tipo=tipo_componente,
                                        codigo=codigo_componente, nivel=nivel_componente, nome=nome_componente,
                                        ch_teorica=ch_teorico, ch_pratica=ch_pratico, ch_estagio=ch_estagio,
                                        ch_total=ch_total, ch_docente=ch_dedicada_docente, ch_ead=ch_ead,
                                        cr_max_ead=cr_max_ead, equivalencia=equivalencia,
                                        requisito=pre_requisito, corequisito=co_requisito, ementa=ementa,
                                        modalidade=modalidade, departamento=depto)
            cc.save()
        else:
            cc_antigo, atualizacoes = atualizar_componente_curricular(
                id_componente, tipo_componente, codigo_componente, nivel_componente, nome_componente,
                ch_teorico, ch_pratico, ch_estagio, ch_total, ch_dedicada_docente, ch_ead, cr_max_ead,
                equivalencia, pre_requisito, co_requisito, ementa, modalidade, depto
            )
            if cc_antigo and atualizacoes:
                componentes_atualizados_set.add(str(cc_antigo) + ', ' + str(atualizacoes))
            else:
                print('.', end="")


if __name__ == "__main__":
    main()