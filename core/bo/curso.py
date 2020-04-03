from core.models import Curso


def get_cursos():
    """
        Lista todos os cursos. Retorna apenas cursos do CERES.
    """
    return Curso.objects.all()
