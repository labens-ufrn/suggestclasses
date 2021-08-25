import django
django.setup()
from core.bo.sistemas import get_estrutura_sistemas, get_estrutura_sistemas_dct
from core.models import EstruturaCurricular, OrganizacaoCurricular, ComponenteCurricular, Curso
from dados.service.estrutura_service import STATUS_ATIVA, STATUS_INATIVA


def main():
    print("Criando Organizações Modificadas - SuggestClasses ...!")
    adicionar_componentes_pedagogia()
    criar_estrutura_sistemas_dct()
    criar_organizacao_sistemas_dct()


def criar_estrutura_sistemas_dct():
    print("\nCriar Estrutura de Sistemas 01B - Códigos DCT")
    if not EstruturaCurricular.objects.filter(id_curriculo=510230608).exists():
        curso_sistemas = Curso.objects.get(codigo=7191770)
        EstruturaCurricular.objects.create(
            id_curriculo=510230608, codigo='01B',
            nome='SISTEMAS DE INFORMAÇÃO - CAICÓ - MT - BACHARELADO',
            semestre_conclusao_minimo=8, semestre_conclusao_ideal=8,
            semestre_conclusao_maximo=12, meses_conclusao_minimo=None,
            meses_conclusao_ideal=None, meses_conclusao_maximo=None, cr_total_minimo=148,
            ch_total_minima=3000, ch_optativas_minima=300, ch_complementar_minima=180,
            max_eletivos=240, ch_nao_atividade_obrigatoria=2220,
            cr_nao_atividade_obrigatorio=148, ch_atividade_obrigatoria=480,
            cr_minimo_semestre=8, cr_ideal_semestre=24, cr_maximo_semestre=28,
            ch_minima_semestre=120, ch_ideal_semestre=None, ch_maxima_semestre=0,
            periodo_entrada_vigor=1, ano_entrada_vigor=2015,
            observacao='', status=STATUS_ATIVA, curso=curso_sistemas)


def criar_organizacao_sistemas_dct():
    print("\nPovoar Componentes de Sistemas com Código DCT")
    bsi_ec_dcea = get_estrutura_sistemas()
    bsi_ec_dcea.status = STATUS_INATIVA
    bsi_ec_dcea.save()

    bsi_ec_dct = get_estrutura_sistemas_dct()
    bsi_ec_dct.status = STATUS_ATIVA
    bsi_ec_dct.save()

    org_bsi_dcea = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec_dcea)

    id_curriculo_componente = 521273697  # O maior na planilha 421273697

    for org in org_bsi_dcea:
        id_curriculo_componente += 1

        # buscar componente DCT se existir
        cod_original = org.componente.codigo
        dep = cod_original[:3]
        num = cod_original[3:]

        if (dep == 'BSI' and (num != '5001' and num != '5002')) or cod_original == 'CEA0008':
            cod_dct = 'DCT' + num
            # print('Código do Componente DCT: ' + cod_dct)
            if ComponenteCurricular.objects.filter(codigo=cod_dct).exists():
                cc = ComponenteCurricular.objects.get(codigo=cod_dct)
            else:
                print('\nERROR - Componente não existe: ' + cod_dct + ' - ' + org.componente.nome)
                cc = ComponenteCurricular.objects.get(codigo=cod_original)

        else:
            # print(cod_original)
            cc = ComponenteCurricular.objects.get(codigo=cod_original)

        if not OrganizacaoCurricular.objects.filter(estrutura=bsi_ec_dct, componente=cc).exists():
            oc = OrganizacaoCurricular(id_curriculo_componente=id_curriculo_componente, estrutura=bsi_ec_dct,
                                       componente=cc, semestre=org.semestre, tipo_vinculo=org.tipo_vinculo,
                                       nivel=org.nivel)
            oc.save()
        print('.', end="")


def adicionar_componentes_pedagogia():
    print("Povoar Componentes de Pedagogia - Estrutura Antiga")
    id_ec = 133495154
    ped_ec = EstruturaCurricular.objects.get(id_curriculo=id_ec)

    id_curriculo_componente = 521274786  # O maior na planilha 521273786

    componentes = get_componentes()

    for cc in componentes:
        id_curriculo_componente += 1

        if not OrganizacaoCurricular.objects.filter(estrutura=ped_ec, componente=cc):
            oc = OrganizacaoCurricular(id_curriculo_componente=id_curriculo_componente, estrutura=ped_ec,
                                       componente=cc, semestre=0, tipo_vinculo='OPTATIVO', nivel='GRADUAÇÃO')
            oc.save()
        print('.', end="")


def get_componentes():
    lista = []
    # 8° período
    # DED0437 - ARTE E EDUCAÇÃO - 60h
    cc = ComponenteCurricular.objects.get(codigo='DED0437')
    lista.append(cc)
    # DED0438 - MONOGRAFIA I - 30h
    cc = ComponenteCurricular.objects.get(codigo='DED0438')
    lista.append(cc)
    # DED0439 - EDUCAÇÃO E AVALIAÇÃO - 60h
    cc = ComponenteCurricular.objects.get(codigo='DED0439')
    lista.append(cc)
    # DED0440 - EDUCAÇÃO A DISTÂNCIA - 90h
    cc = ComponenteCurricular.objects.get(codigo='DED0440')
    lista.append(cc)

    # 6° período
    # DED0428 - LÍNGUA BRASILEIRA DE SINAIS - LIBRAS - 90h
    cc = ComponenteCurricular.objects.get(codigo='DED0428')
    lista.append(cc)
    # DED0429 - LINGUA PORT. NO ENSINO FUNDAMENTAL
    cc = ComponenteCurricular.objects.get(codigo='DED0429')
    lista.append(cc)
    # DED0430 - GEOGRAFIA NO ENSINO FUNDAMENTAL - 90h
    cc = ComponenteCurricular.objects.get(codigo='DED0430')
    lista.append(cc)
    # DED0431 - HISTORIA NO ENSINO FUNDAMENTAL - 90h
    cc = ComponenteCurricular.objects.get(codigo='DED0431')
    lista.append(cc)
    # DED0632 - ESTAGIO III ( ENSINO FUNDAMENTAL) - 75h
    cc = ComponenteCurricular.objects.get(codigo='DED0632')
    lista.append(cc)
    # DED0632 - ESTAGIO III ( ENSINO FUNDAMENTAL) - 75h
    cc = ComponenteCurricular.objects.get(codigo='DED0632')
    lista.append(cc)

    return lista


if __name__ == "__main__":
    main()
