from core.models import ComponenteCurricular, EstruturaCurricular, OrganizacaoCurricular


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


def get_semestres_by_curso(curso):
    semestres = OrganizacaoCurricular.objects.filter(estrutura__curso=curso) \
                    .values_list('semestre', 'semestre').distinct().order_by('semestre')
    return semestres


def get_componentes_by_curso(curso):
    componentes = OrganizacaoCurricular.objects.filter(estrutura__curso=curso) \
                    .values('componente')
    return componentes


def get_componentes_by_curso(curso, semestre):
    oc = OrganizacaoCurricular.objects.filter(
        estrutura__curso=curso, estrutura__status=EstruturaCurricular.ATIVA, semestre=semestre) \
                    .values_list('componente', flat=True)
    componentes = ComponenteCurricular.objects.filter(pk__in=oc).order_by('nome', 'codigo')
    return componentes