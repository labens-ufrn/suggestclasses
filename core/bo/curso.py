from core.models import Curso


def get_cursos():
    """
        Lista todos os cursos. Retorna apenas cursos do CERES.
    """
    return Curso.objects.all()


def get_curso_by_codigo(codigo):
    """
        Retorna apenas o curso de mesmo código.
    """
    return Curso.objects.get(codigo=codigo)
