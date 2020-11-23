from core.models import Historico


def criar_historico(discente, componente):
    historico = Historico.objects.create(discente=discente, componente=componente)
    return historico


def listar_historicos():
    historicos = Historico.objects.all()
    return historicos


def listar_historicos_by_discente(discente):
    historicos = Historico.objects.filter(discente=discente)
    return historicos

def excluir_historico(discente, componente):
    try:
        Historico.objects.get(discente=discente, componente=componente).delete()
        return True
    except Historico.DoesNotExist:
        return False
    