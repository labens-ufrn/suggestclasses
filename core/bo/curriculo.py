from core.models import OrganizacaoCurricular


def get_curriculo_by_cc(id_componente_curricular):
    """
        Retorna uma Organização Curricular (Currículo) que contenha o componente. O currículo é a combinação de
        componentes curriculares vinculados a uma Estrutura Curricular
    :param id_componente_curricular: Identificador do Componente Curricular
    :return: Um ou mais objetos de Organização Curricular
    """
    curriculo = None
    if id_componente_curricular != '' and \
       OrganizacaoCurricular.objects.filter(componente__id_componente=id_componente_curricular).exists():
        curriculo = OrganizacaoCurricular.objects.filter(componente__id_componente=id_componente_curricular)
    return curriculo
