from datetime import datetime

import pytz
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404

from core.forms import VotoTurmaForm
from core.models import Enquete, VotoTurma, ComponenteCurricular
from core.visoes.suggest_view import discente_existe, redirecionar


def enquete_voto_view(request, pk, abstencao=None):
    usuario = request.user
    if not discente_existe(usuario):
        messages.error(request, 'Não há um discente relacionado ao usuário.')
        return redirecionar(request)
    discente = check_discente(request)

    enquete = Enquete.objects.get(pk=pk)

    url_redirect = check_periodo_enquete(request, enquete)
    if url_redirect:
        return url_redirect

    mesmo_curso = check_curso(enquete, discente)
    if not mesmo_curso:
        messages.error(request, 'Você não pode votar na enquete "' + enquete.nome + '".')
        return redirect('/core/enquetes/list')

    if request.method == "POST":
        form_voto = VotoTurmaForm(request.POST, enquete=enquete)

        if form_voto.is_valid() and tem_componente(form_voto):
            voto_turma = form_voto.save(commit=False)
            voto_turma_carregar(enquete, discente, voto_turma, VotoTurma.VALIDO)

            if voto_permitido(request, enquete, discente, voto_turma.componente):
                enquete_deletar_votos_discente(request, enquete, discente, abstencao=True   )
                voto_turma.save()
                messages.success(request, 'Voto cadastrada com sucesso.')
                return redirect('/core/enquetes/' + str(enquete.pk) + '/votar')
        messages.error(request, form_voto.errors)
    elif abstencao and voto_permitido(request, enquete, discente):
        voto_turma = VotoTurma()
        voto_turma_carregar(enquete, discente, voto_turma, VotoTurma.ABSTENCAO)
        enquete_deletar_votos_discente(request, enquete, discente)
        voto_turma.save()
        messages.success(request, 'Abstenção cadastrada com sucesso.')
        return redirect('/core/enquetes/' + str(enquete.pk) + '/votar')
        form_voto = VotoTurmaForm(enquete=enquete)
    else:
        form_voto = VotoTurmaForm(enquete=enquete)

    qtd_votos = get_qtd_votos(enquete, discente)
    votos_por_discente = get_votos(enquete, discente)
    context = {
        'enquete': enquete,
        'qtd_votos': qtd_votos,
        'form_voto': form_voto,
        'votos_por_discente': votos_por_discente,
    }
    return render(request, 'core/enquetes/votar.html', context)


def enquete_detalhar_voto_view(request, pk, abstencao=None):
    usuario = request.user
    if not discente_existe(usuario):
        messages.error(request, 'Não há um discente relacionado ao usuário.')
        return redirecionar(request)
    discente = check_discente(request)
    enquete = Enquete.objects.get(pk=pk)

    qtd_votos = get_qtd_votos(enquete, discente)
    votos_por_discente = get_votos(enquete, discente)
    context = {
        'enquete': enquete,
        'qtd_votos': qtd_votos,
        'votos_por_discente': votos_por_discente,
    }
    return render(request, 'core/enquetes/detalhar_voto.html', context)


def tem_componente(form_voto):
    if form_voto.cleaned_data['componente']:
        return True
    form_voto.add_error('componente', 'Selecione um Componente Curricular para votar.')
    return False


def voto_turma_carregar(enquete, discente, voto_turma, tipo):
    voto_turma.discente = discente
    voto_turma.enquete = enquete
    voto_turma.tipo = tipo


def check_discente(request):
    usuario = request.user
    if not discente_existe(usuario):
        messages.error(request, 'Não há um discente relacionado ao usuário.')
        return redirecionar(request)
    return usuario.discente


def voto_permitido(request, enquete, discente, componente=None):
    existe_voto = False
    if componente:
        existe_voto = voto_existe(enquete, discente, componente)
    votou_max = votou(enquete, discente)
    mesmo_curso = check_curso(enquete, discente)

    if existe_voto:
        messages.error(request, 'Você já votou neste componente curricular!')
    if votou_max:
        messages.error(request, 'Você já votou ' + str(enquete.numero_votos) + ' vezes, máximo permitido!')
    if not mesmo_curso:
        messages.error(request, 'Você só pode votar em Enquetes do seu curso!')
    return not existe_voto and not votou_max and mesmo_curso


def voto_existe(enquete, discente, componente):
    votos = VotoTurma.objects.filter(enquete=enquete, discente=discente, componente=componente)
    if votos.exists():
        return True
    return False


def votou(enquete, discente):
    num_votos = get_qtd_votos(enquete, discente)
    if num_votos < enquete.numero_votos:
        return False
    return True


def check_curso(enquete, discente):
    if enquete.curso.nome == discente.nome_curso:
        return True
    return False


def get_qtd_votos(enquete, discente):
    num_votos = VotoTurma.objects.filter(enquete=enquete, discente=discente).count()
    return num_votos


def get_votos(enquete, discente):
    votos = VotoTurma.objects.filter(enquete=enquete, discente=discente)
    return votos


@permission_required("core.delete_vototurma", login_url='/core/usuario/logar', raise_exception=True)
def enquete_deletar_voto_discente(request, pk, template_name='core/enquetes/voto_confirm_delete.html'):
    voto_turma = get_object_or_404(VotoTurma, pk=pk)
    if not tem_permissao(request, voto_turma.discente):
        messages.error(request, 'Você não tem permissão de Excluir este voto.')
        return redirecionar(request)
    url_redirect = check_periodo_enquete(request, voto_turma.enquete)
    if url_redirect:
        return url_redirect
    if request.method == 'POST':
        voto_turma.delete()
        messages.success(request, 'Voto na enquete excluído com sucesso.')
        return redirecionar(request)
    return render(request, template_name, {'object': voto_turma})


@permission_required("core.delete_vototurma", login_url='/core/usuario/logar', raise_exception=True)
def enquete_deletar_votos_discente(request, enquete, discente, abstencao=None):
    if not tem_permissao(request, discente):
        messages.error(request, 'Você não tem permissão de Excluir votos.')
        return redirecionar(request)
    if abstencao:
        VotoTurma.objects.filter(enquete=enquete, discente=discente, tipo=VotoTurma.ABSTENCAO).delete()
    else:
        VotoTurma.objects.filter(enquete=enquete, discente=discente).delete()


def tem_permissao(request, discente_voto):
    usuario = request.user
    if not discente_existe(usuario):
        messages.error(request, 'Não há um discente relacionado ao usuário.')
        return redirecionar(request)
    discente = usuario.discente
    if discente == discente_voto:
        return True
    return False


def get_qtd_votantes(enquete):
    qtd_votantes = len(set(VotoTurma.objects.filter(enquete=enquete).values_list('discente')))
    return qtd_votantes


def get_qtd_abstencao(enquete):
    qtd_votantes = len(set(VotoTurma.objects.filter(
        enquete=enquete, tipo=VotoTurma.ABSTENCAO).values_list('discente')))
    return qtd_votantes


def load_componente(request):
    componente_id = request.GET.get('componenteId')
    componente = ComponenteCurricular.objects.get(pk=componente_id)
    return render(request, 'core/enquetes/requisitos_list.html', {'componente': componente})


def check_periodo_enquete(request, enquete):
    agora = datetime.now()
    utc = pytz.UTC
    if enquete.data_hora_inicio.replace(tzinfo=utc) > agora.replace(tzinfo=utc) \
       or agora.replace(tzinfo=utc) > enquete.data_hora_fim.replace(tzinfo=utc):
        messages.error(request, 'Voto fora do período da Enquete "' + enquete.nome + '".')
        return redirect('/core/enquetes/list')
    return None
