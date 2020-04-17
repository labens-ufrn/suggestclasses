from core.bo.sevices import get_estrutura_by_id
from core.models import OrganizacaoCurricular, ComponenteCurricular


def get_estrutura_sistemas():
    id_ec = 510230607
    bsi_ec = get_estrutura_by_id(id_ec)
    return bsi_ec


def get_estrutura_sistemas_dct():
    id_ec = 510230608
    bsi_ec = get_estrutura_by_id(id_ec)
    return bsi_ec


def criar_organizacao_sistemas_dct():
    bsi_ec_dcea = get_estrutura_sistemas()
    bsi_ec_dct = get_estrutura_sistemas_dct()

    org_bsi_dcea = OrganizacaoCurricular.objects.filter(estrutura=bsi_ec_dcea)

    id_curriculo_componente = 521273697  # O maior na planilha 421273697

    for org in org_bsi_dcea:
        id_curriculo_componente += 1

        # buscar componente DCT se existir
        cod_original = org.componente.codigo
        dep = cod_original[:3]
        num = cod_original[3:]

        if dep == 'BSI' and (num != '5001' and num != '5002'):
            cod_dct = 'DCT' + num
            # print('Código do Componente DCT: ' + cod_dct)
            if ComponenteCurricular.objects.filter(codigo=cod_dct).exists():
                cc = ComponenteCurricular.objects.get(codigo=cod_dct)
            else:
                print('ERROR - Componente não existe: ' + cod_dct + ' - ' + org.componente.nome)
        else:
            # print(cod_original)
            cc = ComponenteCurricular.objects.get(codigo=cod_original)

        if not OrganizacaoCurricular.objects.filter(estrutura=bsi_ec_dct, componente=cc):
            oc = OrganizacaoCurricular(id_curriculo_componente=id_curriculo_componente, estrutura=bsi_ec_dct,
                                       componente=cc, semestre=org.semestre, tipo_vinculo=org.tipo_vinculo,
                                       nivel=org.nivel)
            oc.save()
