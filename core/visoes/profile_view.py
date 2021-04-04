


from core.models import Historico
from core.bo.curso import get_curso_by_codigo
from core.bo.curriculo import get_componentes_by_curso, get_componentes_by_curso_semestre
from core.forms import HistoricoForm
from django.shortcuts import get_object_or_404, render
from core.bo.docente import carrega_turmas_por_horario
from core.bo.historico import listar_historicos_by_discente
from core.visoes.suggest_view import criar_string, discente_existe, discente_grade_horarios, docente_existe, docente_grade_horarios, get_solicitacoes, redirecionar
from django.contrib import messages
from core.bo.periodos import get_periodo_ativo, get_periodo_planejado
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url='/accounts/login')
def profile(request, username):
    periodo_letivo_atual = get_periodo_ativo()
    periodo_letivo_planejado = get_periodo_planejado()
    usuario = User.objects.get(username=username)

    if request.user != usuario:
        messages.error(request, 'Você não tem permissão de visualizar esse Perfil.')
        return redirecionar(request)

    horarios_atual = None
    horarios = None
    semestres = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    solicitacao_list = None
    historico = None
    form_historico = None
    tab_active = 'usuario'

    if discente_existe(usuario):
        perfil = usuario.discente
        perfil_link = 'core/usuario/profile_discente.html'
        grupos = criar_string(usuario.groups.all())
        horarios = discente_grade_horarios(
            perfil, periodo_letivo_planejado.ano, periodo_letivo_planejado.periodo)
        solicitacao_list = get_solicitacoes(
            perfil, periodo_letivo_planejado.ano, periodo_letivo_planejado.periodo)
        historico = listar_historicos_by_discente(perfil)
        if request.method == "POST":
            form_historico = HistoricoForm(request.POST, discente=perfil)
            tab_active = 'historico'
            if form_historico.is_valid():
                add_historico = form_historico.save(commit=False)
                add_historico.discente = perfil
                add_historico.save()
                messages.success(request, 'Componente cadastrado no histórico com sucesso.')
            else:
                messages.error(request, form_historico.errors['__all__'])
        else:
            form_historico = HistoricoForm(discente=perfil)
    elif docente_existe(usuario):
        perfil = usuario.docente
        perfil_link = 'core/usuario/profile_docente.html'
        grupos = criar_string(usuario.groups.all())
        horarios_atual = carrega_turmas_por_horario(
            perfil, periodo_letivo_atual.ano, periodo_letivo_atual.periodo)
        horarios = docente_grade_horarios(
            perfil, periodo_letivo_planejado.ano, periodo_letivo_planejado.periodo, semestres)
    else:
        perfil = None
        perfil_link = 'core/usuario/profile.html'
        tab_active = 'usuario'
        grupos = criar_string(usuario.groups.all())

    context = {
        'usuario': usuario,
        'grupos': grupos,
        'perfil': perfil,
        'horarios_atual': horarios_atual,
        'horarios': horarios,
        'ano_periodo_atual': periodo_letivo_atual,
        'ano_periodo': periodo_letivo_planejado,
        'solicitacao_deletar_link': 'solicitacao_deletar',
        'solicitacao_list': solicitacao_list,
        'historico_discente': historico,
        'form_historico': form_historico,
        'tab_active': tab_active,
    }

    return render(request, perfil_link, context)


def load_componentes_historico(request):
    semestre_id = request.GET.get('semestre_id')
    curso_id = request.GET.get('curso_id')
    curso = get_curso_by_codigo(curso_id)
    componentes = get_componentes_by_curso_semestre(curso=curso, semestre=semestre_id)
    return render(request, 'core/usuario/componentes_list_option.html', {'componentes': componentes})

def historico_deletar_componente(request, pk, template_name='core/usuario/confirm_delete_historico.html'):
    historico = get_object_or_404(Historico, pk=pk)
    if not verificar_permissoes(request, historico):
        messages.error(request, 'Você não tem permissão de Excluir este Histórico.')
        return redirecionar(request)
    if request.method == 'POST':
        historico.delete()
        messages.success(request, 'Histórico excluído com sucesso.')
        return redirecionar(request)
    return render(request, template_name, {'object': historico})


def verificar_permissoes(request, historico):
    usuario = request.user
    if historico.discente.usuario == usuario:
        return True
    return False
