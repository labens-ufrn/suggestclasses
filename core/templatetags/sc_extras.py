from django import template

register = template.Library()


@register.simple_tag
def get_curriculo(turma, estrutura):
    curriculos = turma.get_curriculos()
    if curriculos.count() > 1:
        return curriculos.first()
    return curriculos.first()


@register.simple_tag
def get_semestre(turma, estrutura):
    curriculo = turma.get_curriculos(estrutura)
    if curriculo:
        return curriculo.semestre
    return None


@register.simple_tag
def get_tipo_vinculo(turma, estrutura):
    curriculo = turma.get_curriculos(estrutura)
    if curriculo:
        return curriculo.tipo_vinculo
    return None
