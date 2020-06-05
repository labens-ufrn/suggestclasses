from core.models import Enquete


def get_enquetes():
    """
        Lista todos as Enquetes.
    """
    return Enquete.objects.all().order_by('curso', 'nome', 'periodo')
