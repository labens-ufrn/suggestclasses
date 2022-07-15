import json
import logging
from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from core.bo.docente import get_funcao_by_siape
from core.bo.periodos import get_periodo_ativo, get_periodo_planejado
from core.bo.sevices import get_organizacao_by_componente
from core.bo.sugestao import solicitacao_incluir, solicitacao_verificar_choques
from core.bo.turma import atualiza_exibicao, atualiza_semestres, carrega_sugestao_turmas, converte_desc_horario, \
    TurmaHorario, carrega_sugestao_horario
from core.config.config import get_config
from core.forms import SugestaoTurmaForm
from core.models import SugestaoTurma, SolicitacaoTurma, Horario, Docente, VinculoDocenteSugestao
from suggestclasses.settings import DOMAINS_WHITELIST

logger = logging.getLogger('suggestclasses.logger')
config = get_config()


def sugestao_grade_horarios(request, estrutura, sugestao_incluir_link, sugestao_manter_link, sugestao_list_link):
    semestres = request.GET.getlist('semestres')
    semestres = atualiza_semestres(semestres)
    ano_periodo_atual = get_periodo_ativo()
    ano_periodo_prox = get_periodo_planejado()
    ano_periodo = request.GET.getlist('ano_periodo')
    if ano_periodo is None or ano_periodo == []:
        ano_periodo = ano_periodo_prox
    elif ano_periodo_atual.is_same_as(ano_periodo[0]):
        ano_periodo = ano_periodo_atual
    else:
        ano_periodo = ano_periodo_prox

    docente_sel = request.GET.getlist('docente_sel')
    docente_obj: Docente = None
    if docente_sel is not None and docente_sel != []:
        docente_sel = docente_sel[0]
        docente_obj = Docente.objects.filter(nome=docente_sel).first()
    else:
        docente_sel = ""

    tt = carrega_sugestao_horario(ano_periodo.ano, ano_periodo.periodo,
                                  curso=estrutura.curso, semestres=semestres, docente=docente_obj)
    context = {
        'tt': tt,
        'estrutura': estrutura,
        'ano_periodo_atual': ano_periodo_atual,
        'ano_periodo_prox': ano_periodo_prox,
        'ano_periodo_sel': ano_periodo,
        'semestres': atualiza_exibicao(semestres),
        'semestres_atual': criar_string(semestres) + '.',
        'sugestao_incluir_link': sugestao_incluir_link,
        'sugestao_manter_link': sugestao_manter_link,
        'sugestao_list_link': sugestao_list_link,
        'docentes': Docente.objects.all(),
        'docente_sel': docente_sel
    }

    return render(request, 'core/sugestao/grade_horarios.html', context)


def sugestao_manter(request, estrutura, sugestao_incluir_link, sugestao_grade_link,
                    sugestao_editar_link, sugestao_deletar_link):
    """
            Lista todas as salas do centro.
    """
    # Todos os Semestres
    semestres = ['100']
    semestres = atualiza_semestres(semestres)

    periodo_letivo = get_periodo_planejado()

    st_list = carrega_sugestao_turmas(estrutura, semestres, periodo_letivo.ano, periodo_letivo.periodo)
    st_list = sorted(st_list, key=lambda sc: sc.componente.nome)

    context = {
        'periodo_letivo': periodo_letivo,
        'estrutura': estrutura,
        'sugestao_incluir_link': sugestao_incluir_link,
        'sugestao_editar_link': sugestao_editar_link,
        'sugestao_deletar_link': sugestao_deletar_link,
        'sugestao_grade_link': sugestao_grade_link,
        'sugestao_list': st_list
    }

    return render(request, 'core/sugestao/manter.html', context)


def sugestao_incluir(request, estrutura, sugestao_manter_link):
    periodo_letivo = get_periodo_planejado()
    vinculos = []
    if request.method == "POST":
        form_sugestao = SugestaoTurmaForm(request.POST, estrutura=estrutura)
        vinculos_docente = request.POST.get('vinculos_docente')
        vinculos = carregar_vinculos(vinculos_docente)

        if form_sugestao.is_valid():
            sugestao_turma = form_sugestao.save(commit=False)
            carregar_dados(request, sugestao_turma, estrutura)
            horarios_list = converte_desc_horario(sugestao_turma.descricao_horario)
            if not verificar_existencia(form_sugestao, sugestao_turma) \
               and not verificar_choques(form_sugestao, sugestao_turma, horarios_list):
                sugestao_turma.save()
                vinculos_docente_salvar(sugestao_turma, vinculos)
                atualizar_horarios(sugestao_turma, horarios_list)
                messages.success(request, 'Sugestão de Turma cadastrada com sucesso.')
                return redirect(sugestao_manter_link)
        messages.error(request, form_sugestao.errors)
    else:
        form_sugestao = SugestaoTurmaForm(estrutura=estrutura)

    context = {
        'periodo_letivo': periodo_letivo,
        'estrutura': estrutura,
        'form_sugestao': form_sugestao,
        'vinculos': vinculos,
    }
    return render(request, 'core/sugestao/incluir.html', context)


def atualizar_horarios(sugestao, novos_horarios):
    # limpa o conjunto de horários
    sugestao.horarios.clear()
    # adiciona os novos horários
    sugestao.horarios.set(novos_horarios)


def carregar_dados(request, sugestao_turma, estrutura):
    periodo_letivo = get_periodo_planejado()

    sugestao_turma.tipo = 'REGULAR'
    sugestao_turma.ano = periodo_letivo.ano
    sugestao_turma.periodo = periodo_letivo.periodo
    sugestao_turma.campus_turma = estrutura.curso.centro.sigla
    if sugestao_turma.local:
        sugestao_turma.campus_turma = sugestao_turma.local.campus
    sugestao_turma.criador = request.user
    sugestao_turma.total_solicitacoes = 0

    org_curricular = get_organizacao_by_componente(estrutura, sugestao_turma.componente)
    sugestao_turma.semestre = org_curricular.first().semestre
    sugestao_turma.tipo_vinculo = org_curricular.first().tipo_vinculo
    sugestao_turma.curso = estrutura.curso


def verificar_existencia(form_sugestao, sugestao_turma):
    sugestoes = SugestaoTurma.objects.filter(
        codigo_turma=sugestao_turma.codigo_turma,
        componente=sugestao_turma.componente,
        ano=sugestao_turma.ano,
        periodo=sugestao_turma.periodo).values('codigo_turma')
    if sugestoes.exists():
        sugestoes = SugestaoTurma.objects.filter(
            componente=sugestao_turma.componente,
            ano=sugestao_turma.ano,
            periodo=sugestao_turma.periodo).values_list('codigo_turma')
        codigos_str = criar_string(sugestoes)
        form_sugestao.add_error('codigo_turma',
                                'Os seguintes códigos de turmas já foram utilizados: ' + codigos_str + '.')
        return True
    return False


def verificar_choques(form_sugestao, sugestao_turma, horarios_list):
    choques_componentes = set()
    choques_componentes_semestre = set()
    choques_horarios = []
    choques_semestres = []
    choque_docente = []
    periodo_letivo = get_periodo_planejado()
    for horario in horarios_list:
        sugestoes = horario.sugestoes.all().filter(
            ano=periodo_letivo.ano, periodo=periodo_letivo.periodo)
        if sugestoes:
            for s in sugestoes:
                if s.codigo_turma == sugestao_turma.codigo_turma and s.componente == sugestao_turma.componente:
                    break
                if sugestao_turma.local is not None and s.local == sugestao_turma.local:
                    choques_componentes.add(str(s.componente.codigo) + ' - ' + s.componente.nome)
                    choques_horarios.append(horario.dia + horario.turno + horario.ordem)
                if sugestao_turma.docente is not None and s.docente == sugestao_turma.docente:
                    choques_componentes.add(str(s.componente.codigo) + ' - ' + s.componente.nome)
                    choque_docente.append(horario.dia + horario.turno + horario.ordem)

                verificar_choques_semestre(form_sugestao, horario, s, sugestao_turma, choques_componentes_semestre, choques_semestres)

    if choques_horarios or choque_docente or choques_componentes or choques_semestres:
        if choques_componentes:
            form_sugestao.add_error('componente',
                                    'Choque com os Componentes Curriculares: ' +
                                    criar_string(list(choques_componentes)) + '.')
        if choques_horarios:
            form_sugestao.add_error('local',
                                    'Sala com choque nos horários: ' +
                                    criar_string(choques_horarios) + '.')
        if choque_docente:
            form_sugestao.add_error('docente',
                                    'Docente com choque nos horários: ' +
                                    criar_string(choque_docente) + '.')
        if choques_semestres:
            form_sugestao.add_error('componente',
                                    'Choque com os Componentes Curriculares do mesmo semestre: ' +
                                    criar_string(list(choques_componentes_semestre)) + '.')
            form_sugestao.add_error('descricao_horario', 'Choque nos horários: ' +
                                    criar_string(choques_semestres) + '.')
        return True
    return False


def verificar_choques_semestre(form_sugestao, horario, sugestao_existente, nova_sugestao, choques_componentes_semestre, choques_semestres):
    checked = form_sugestao.cleaned_data['checked']
    if (sugestao_existente.semestre == nova_sugestao.semestre) and \
                    ((nova_sugestao.semestre != 0) or \
                     (nova_sugestao.semestre == 0 and checked)):
        choques_componentes_semestre.add(
            str(sugestao_existente.componente.codigo) + ' - ' +
                sugestao_existente.componente.nome)
        choques_semestres.append(horario.dia + horario.turno + horario.ordem)


def criar_string(colecao):
    str_result = ''
    tam = len(colecao)
    for index, s in enumerate(colecao, start=1):
        str_result += s.__str__()
        if tam > 1 and index < tam:
            str_result += ', '
    str_result += ''
    return str_result


@permission_required("core.change_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_editar(request, pk, estrutura, template_name='core/sugestao/editar.html'):
    sugestao = get_object_or_404(SugestaoTurma, pk=pk)
    if not verificar_permissoes(request, sugestao, estrutura):
        messages.error(request, 'Você não tem permissão de Editar esta Sugestão de Turma.')
        return redirecionar(request)
    form_sugestao = SugestaoTurmaForm(request.POST or None, instance=sugestao, estrutura=estrutura)
    vinculos_docente = request.POST.get('vinculos_docente')
    if vinculos_docente is not None:
        vinculos = carregar_vinculos(vinculos_docente)
    else:
        vinculos = load_vinculos_docentes(sugestao)
    if form_sugestao.is_valid():
        sugestao_turma = form_sugestao.save(commit=False)
        horarios_list = converte_desc_horario(sugestao_turma.descricao_horario)
        if not verificar_choques(form_sugestao, sugestao_turma, horarios_list):
            sugestao_turma.save()
            sugestao_turma.horarios.clear()  # limpa o conjunto de horários
            sugestao_turma.horarios.set(horarios_list)  # adiciona os novos horários
            vinculos_docente_salvar(sugestao_turma, vinculos)
            messages.success(request, 'Sugestão de Turma alterada com sucesso.')
            return redirecionar(request)
    else:
        messages.error(request, form_sugestao.errors)
    return render(request, template_name,
                  {'form': form_sugestao, 'vinculos': vinculos})


@permission_required("core.delete_sugestaoturma", login_url='/core/usuario/logar', raise_exception=True)
def sugestao_deletar(request, pk, estrutura, template_name='core/sugestao/confirm_delete.html'):
    sugestao = get_object_or_404(SugestaoTurma, pk=pk)
    if not verificar_permissoes(request, sugestao, estrutura):
        messages.error(request, 'Você não tem permissão de Excluir esta Sugestão de Turma.')
        return redirecionar(request)
    if request.method == 'POST':
        try:
            sugestao.delete()
            messages.success(request, 'Sugestão de Turma excluída com sucesso.')
        except ProtectedError as err:
            messages.error(request, 'Sugestão de Turma não pode ser excluída. Erro {0}'.format(err))
        return redirecionar(request)
    return render(request, template_name, {'object': sugestao})


@permission_required("core.delete_solicitacaoturma", login_url='/core/usuario/logar', raise_exception=True)
def solicitacao_discente_deletar(request, pk, template_name='core/sugestao/solicitacao_confirm_delete.html'):
    solicitacao = get_object_or_404(SolicitacaoTurma, pk=pk)
    if not tem_permissao(request, solicitacao):
        messages.error(request, 'Você não tem permissão de Excluir esta Solicitacao de Turma.')
        return redirecionar(request)
    if request.method == 'POST':
        solicitacao.delete()
        messages.success(request, 'Solicitação de Turma excluída com sucesso.')
        return redirecionar(request)
    return render(request, template_name, {'object': solicitacao})


def redirecionar(request):
    url = request.GET.get("next", "/")
    parsed_uri = urlparse(url)
    if parsed_uri.netloc == '' or parsed_uri.netloc in DOMAINS_WHITELIST:
        return HttpResponseRedirect(url)
    return HttpResponseRedirect("/core")


def verificar_permissoes(request, sugestao, estrutura):
    # Verificar se o Usuário é o criador da Sugestão de Turma
    usuario = request.user
    departamento = sugestao.componente.departamento
    if is_criador(usuario, sugestao):
        return True
    # Verificar se o Usuário é o Chefe do Departamento da Sugestão de Turma
    if is_chefe(usuario, departamento):
        return True
    # Verificar se o Usuário é o Coordenador do Curso da Sugestão de Turma
    if is_coordenador(usuario, estrutura.curso):
        return True
    return False


def tem_permissao(request, solicitacao):
    # Verificar se o Usuário é o criador da Solicitação de Turma
    usuario = request.user
    if usuario == solicitacao.usuario:
        return True
    return False


def is_criador(usuario, sugestao):
    """
    Verificar se o Usuário é o criador da Sugestão de Turma.
    :param usuario: Usuário autenticado.
    :param sugestao: Sugestão de Turma.
    :return: True se o usuário for o criador da Sugestão de Turma.
    """
    return usuario == sugestao.criador


def is_chefe(usuario, departamento):
    """
    Verificar se o Usuário tem a Função de Chefe de Departamento.
    :param usuario: Usuário autenticado.
    :param departamento: O departamento de interesse.
    :return: True se o usuário for Chefe do Departamento.
    """
    if not docente_existe(usuario):
        return False

    grupo_chefes = Group.objects.get(name='Chefes')
    grupos = usuario.groups.all()

    id_unidade_lotacao = usuario.docente.id_unidade_lotacao
    test_chefe1 = departamento.id_unidade == id_unidade_lotacao

    siape = usuario.docente.siape
    funcao = get_funcao_by_siape(siape)
    id_unidade_designacao = funcao[0].id_unidade_designacao
    test_chefe2 = departamento.id_unidade == id_unidade_designacao

    return grupo_chefes in grupos and test_chefe1 and test_chefe2


def is_coordenador(usuario, curso):
    """
    Verificar se o Usuário tem a Função de Coordenador de Curso.
    :param usuario: Usuário autenticado.
    :param curso: O curso de interesse.
    :return: True se o usuário for Coordenador do Curso.
    """
    if not docente_existe(usuario):
        return False

    grupo_chefes = Group.objects.get(name='Coordenadores')
    grupos = usuario.groups.all()

    siape = usuario.docente.siape
    test_coordenador1 = False
    if curso.coordenador:
        test_coordenador1 = curso.coordenador.siape == siape

    funcoes = get_funcao_by_siape(siape)
    test_coordenador2 = False
    for funcao in funcoes:
        # id_unidade_designacao = funcao.id_unidade_designacao
        # O id_unidade de curso não existe! Existe no arquivo unidades.csv
        # curso.id_unidade == id_unidade_designacao
        test_coordenador2 = test_coordenador2 or 'COORDENADOR DE CURSO' == funcao.atividade

    return grupo_chefes in grupos and (test_coordenador1 and test_coordenador2)


def docente_existe(usuario):
    """
    Verifica se na instância de Usuário existe um Docente relacionado.
    :param usuario: O usuário autenticado.
    :return: True se existir um Docente relacionado.
    """
    try:
        docente = usuario.docente
        return docente is not None
    except ObjectDoesNotExist:
        return False


def atualizar_solicitacao(request, pk):
    usuario = request.user
    if not discente_existe(usuario):
        messages.error(request, 'Não há um discente relacionado ao usuário.')
        return redirecionar(request)
    discente = usuario.discente
    turma = SugestaoTurma.objects.get(pk=pk)

    choques_componentes, choques_horarios, houve_choques = \
        solicitacao_verificar_choques(discente, turma)

    if houve_choques:
        messages.error(request,
                       'A turma ' + str(turma) + ' tem choque com: ' + criar_string(list(choques_componentes)) +
                       ', nos horários: ' + criar_string(list(choques_horarios)) + '.')
        return redirecionar(request)

    resultado, created = solicitacao_incluir(discente, turma)

    if created:
        messages.success(request, 'Solicitação de Interesse na Turma ' +
                         str(resultado.turma) + ' cadastrada com sucesso.')
    else:
        messages.error(request, 'Já existe Solicitação de Interesse na Turma ' +
                       str(resultado.turma) + '.')

    return redirecionar(request)


def discente_existe(usuario):
    """
    Verifica se na instância de Usuário existe um Discente relacionado.
    :param usuario: O usuário autenticado.
    :return: True se existir um Docente relacionado.
    """
    try:
        discente = usuario.discente
        return discente is not None
    except ObjectDoesNotExist:
        return False


def discente_grade_horarios(discente, ano, periodo):
    solicitacoes = get_solicitacoes(discente, ano, periodo)
    turmas_por_horario = carrega_turmas_por_horario(solicitacoes)
    return turmas_por_horario


def docente_grade_horarios(docente, ano, periodo, semestres):
    turmas_por_horario = carrega_sugestao_horario(ano=ano, periodo=periodo, docente=docente, semestres=semestres)
    return turmas_por_horario


def get_solicitacoes(discente, ano, periodo):
    solicitacoes = SolicitacaoTurma.objects.filter(solicitador=discente, turma__ano=ano, turma__periodo=periodo)
    return solicitacoes


def carrega_turmas_por_horario(turmas):
    """
    Carrega uma lista com 16 posições representando os 16 períodos de 50 min de aulas em todos os turnos.
    Cada posição contém outra lista de 5 posições representando os dias da semana.
    :param turmas: Uma lista de Turmas ou Sugestões de Turma.
    :return: Uma lista bidimensional representando a grade de horários com a lista de turmas
    em cada horário.
    """
    tt = []
    tt.extend(carrega_horario_turmas_por_turno(turmas, 'M'))
    tt.extend(carrega_horario_turmas_por_turno(turmas, 'T'))
    tt.extend(carrega_horario_turmas_por_turno(turmas, 'N'))
    return tt


def carrega_horario_turmas_por_turno(turmas, turno):
    """
    Carrega uma lista com 16 posições representando os 16 períodos de 50 min de aulas para um turno.
    Cada posição contém outra lista de 5 posições representando os dias da semana.
    :param turmas: Uma lista de Turmas ou Sugestões de Turma.
    :param turno: Turno selecionado entre as opções M, T e N.
    :return: Uma lista bidimensional representando a grade de horários com a lista de turmas
    em cada horário.
    """
    tt = []
    n = 7
    if turno == 'N':
        n = 5

    for i in range(1, n):
        horarios = Horario.objects.filter(turno=turno, ordem=i).order_by('dia')
        turmas_horario = []
        for h in horarios:
            turmas_por_horario = []
            for t in turmas:
                horarios_solicitacao = list(t.turma.horarios.all())
                if h in horarios_solicitacao:
                    turmas_por_horario.append(t.turma)
            th = TurmaHorario(h, turmas_por_horario)
            turmas_horario.append(th)
        tt.append(turmas_horario)
    return tt


def load_docentes(request):
    departamento_id = request.GET.get('departamento')
    docentes = Docente.objects.filter(departamento_id=departamento_id).order_by('nome')
    return render(request, 'core/sugestao/docentes_list_option.html', {'docentes': docentes})


def check_vinculo_docente(request):
    vinculos_docente = request.GET.get('vinculos_docente')
    vinculos = carregar_vinculos(vinculos_docente)

    # TODO Fazer checagem de choque de horários do docente
    # %20 is space, %5B is '[' and %5D is ']'
    docente_id = request.GET.get('vinculo[docente]')
    horarios = request.GET.get('vinculo[horarios]')
    carga_horaria = request.GET.get('vinculo[carga_horaria]')
    componente_id = request.GET.get('vinculo[componente]')
    codigo_turma = request.GET.get('vinculo[codigo_turma]')

    docente = Docente.objects.get(pk=docente_id)
    existe_docente = False
    houve_choque = False
    for v in vinculos:
        if docente == v['docente']:
            existe_docente = True
            break

    if not existe_docente:
        horarios_list = converte_desc_horario(horarios)
        choques_docente, houve_choque = existe_choques_docente(docente, horarios_list, componente_id, codigo_turma)
        if not houve_choque:
            vinculo = {'docente': docente, 'horarios': horarios, 'carga_horaria': carga_horaria}
            vinculos.append(vinculo)
            print(vinculo)
        else:
            messages.error(request, 'Docente ' + docente.nome + ' com choque nos horários: ' +
                           criar_string(choques_docente) + '.')
    else:
        messages.error(request, 'Docente ' + docente.nome + ' já adicionado à Turma.')

    data = dict()
    data['existe_docente'] = existe_docente
    data['houve_choque'] = houve_choque
    context = {'vinculos': vinculos}
    data['html_vinculos'] = render_to_string('core/sugestao/vinculo_docente_list.html',
                                             context,
                                             request=request
                                             )
    return JsonResponse(data)


def load_vinculos(request):
    vinculos_docente = request.GET.get('vinculos_docente')
    docente_removido = request.GET.get('docente_removido')
    sugestao_id = request.GET.get('sugestao_id')
    remover_vinculo_docente(sugestao_id, docente_removido)
    vinculos = carregar_vinculos(vinculos_docente)
    return render(request, 'core/sugestao/vinculo_docente_list.html', {'vinculos': vinculos})


def carregar_vinculos(vinculos_docente):
    vinculos = []
    if vinculos_docente is not None and vinculos_docente != '':
        vds = json.loads(vinculos_docente)
        for v in vds['vinculos']:
            docente_id = v["docente"]
            horarios = v['horarios']
            carga_horaria = v['carga_horaria']
            docente = Docente.objects.get(pk=docente_id)
            vinculo = {'docente': docente, 'horarios': horarios, 'carga_horaria': carga_horaria}
            vinculos.append(vinculo)
    return vinculos


def load_vinculos_docentes(sugestao):
    vinculos_list = VinculoDocenteSugestao.objects.filter(sugestao=sugestao).all()
    vinculos = []
    for v in vinculos_list:
        horarios = v.descricao_horario
        carga_horaria = v.carga_horaria
        docente = v.docente
        vinculo = {'docente': docente, 'horarios': horarios, 'carga_horaria': carga_horaria}
        vinculos.append(vinculo)
    return vinculos


def existe_choques_docente(docente, horarios_list, componente_id, codigo_turma):
    choque_docente = []
    periodo_letivo = get_periodo_planejado()

    for horario in horarios_list:
        docente_sugestoes = list(horario.sugestoes.all().filter(
            ano=periodo_letivo.ano, periodo=periodo_letivo.periodo
            ).exclude(componente__id=componente_id, codigo_turma=codigo_turma) )

        for ds in docente_sugestoes:
            vinculos_existentes = ds.vinculodocentesugestao_set.all()
            existe = vinculos_existentes.filter(docente__id=docente.id)
            if existe:
                choque_docente.append(horario.dia + horario.turno + horario.ordem)

    if choque_docente:
        return choque_docente, True
    return None, False


def adicionar_vinculo_docente(sugestao, docente, carga_horaria, horarios):
    if docente is not None and sugestao is not None and \
       not VinculoDocenteSugestao.objects.filter(sugestao=sugestao, docente=docente).exists():
        vinculo = VinculoDocenteSugestao(
            docente=docente, sugestao=sugestao, carga_horaria=carga_horaria, descricao_horario=horarios)
        vinculo.save()
        horarios_docente = converte_desc_horario(horarios)
        vinculo.horarios.set(horarios_docente)


def vinculos_docente_salvar(sugestao, vinculos):
    for vinculo in vinculos:
        adicionar_vinculo_docente(sugestao, vinculo['docente'], vinculo['carga_horaria'], vinculo['horarios'])

def remover_vinculo_docente(sugestao, docente):
    if docente is not None and sugestao is not None and \
       VinculoDocenteSugestao.objects.filter(sugestao__id=sugestao, docente__id=docente).exists():
        vinculo = VinculoDocenteSugestao.objects.get(
            docente__id=docente, sugestao__id=sugestao)
        vinculo.delete()
