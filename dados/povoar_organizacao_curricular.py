import django
django.setup()
from core.models import EstruturaCurricular, OrganizacaoCurricular, ComponenteCurricular


def main():
    print("Povoar Componentes de Pedagogia - Estrutura Antiga")
    adicionar_componentes_pedagogia()


def adicionar_componentes_pedagogia():
    id_ec = 133495154
    ped_ec = EstruturaCurricular.objects.get(id_curriculo=id_ec)

    id_curriculo_componente = 521274786  # O maior na planilha 521273786

    componentes = get_componentes()

    for cc in componentes:
        id_curriculo_componente += 1

        oc = OrganizacaoCurricular(id_curriculo_componente=id_curriculo_componente, estrutura=ped_ec,
                                   componente=cc, semestre=0, tipo_vinculo='OPTATIVO', nivel='GRADUAÇÃO')
        oc.save()


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
