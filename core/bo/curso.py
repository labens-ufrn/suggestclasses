from core.models import Centro, Curso


def get_cursos():
    """
        Lista todos os cursos. Retorna apenas cursos do CERES.
    """
    return Curso.objects.all()

def get_cursos_by_centro(centro: Centro):
    """
        Lista os cursos de um centro.
    """
    return Curso.objects.filter(centro=centro)


def get_curso_by_codigo(codigo):
    """
        Retorna apenas o curso de mesmo código.
    """
    return Curso.objects.get(codigo=codigo)
