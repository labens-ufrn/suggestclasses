from django.conf.global_settings import STATIC_ROOT
from django.conf.urls.static import static
from django.urls import path

from suggestclasses.settings import STATIC_URL, MEDIA_URL, MEDIA_ROOT, DEBUG
from . import views
from .visoes import suggest_view
from .visoes import sugestao_letras_view
from .visoes.sugestao_contabeis_view import sugestao_cont_list, sugestao_cont_manter, sugestao_cont_incluir, \
    sugestao_cont_editar, sugestao_cont_deletar

urlpatterns = [
    path('profile/<username>/', views.profile, name='profile'),

    path('usuario/cadastrar', views.cadastrar_usuario, name='Cadastro de Usuário'),
    path('usuario/logar', views.logar_usuario, name='Login de Usuário'),
    path('usuario/deslogar', views.deslogar_usuario, name='Logout de Usuário'),
    path('usuario/alterar_senha', views.alterar_senha, name='Alterar Senha de Usuário'),

    path('', views.index, name='index'),
    path('sobre', views.sobre, name='sobre'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('horarios_list/', views.horarios_list, name='horarios_list'),
    path('<int:horario_id>/', views.detail, name='detail'),
    path('curso/<int:curso_id>/', views.curso_detail, name='curso_detail'),
    path('curso/list/', views.curso_list, name='Lista de Cursos'),
    path('departamento/list/', views.departamento_list, name='Lista de Departamentos'),
    path('componente/list/', views.componente_list, name='Lista de Componentes Curriculares'),
    path('componentes/<int:pk>/', views.ComponenteDetailView.as_view(), name='componente_detalhar'),

    path('curriculo/list/', views.curriculo_list, name='Lista de Estruturas Curriculares'),
    path('docentes/list/', views.docentes_list, name='docentes_list'),
    path('docente/<int:pk>/', views.DocenteDetailView.as_view(), name='docente_detalhar'),

    path('salas/list/', views.search_salas, name='search_salas'),
    path('enquetes/list/', views.search_enquetes, name='search_enquetes'),
    path('enquetes/<int:pk>/', views.EnqueteDetailView.as_view(), name='enquete_detalhar'),
    path('enquetes/<int:pk>/componente/<int:cc_pk>/', views.enquete_votos_listar, name='enquete_votos_listar'),
    path('enquetes/<int:pk>/votar', views.enquete_votar, name='enquete_votar'),
    path('enquetes/<int:pk>/votos/manter', views.sugestao_solicitar, name='enquete_votos_manter'),
    path('enquetes/deletar/votos/<int:pk>/', views.enquete_deletar_voto, name='enquete_deletar_voto'),

    path('flow/', views.flow_list, name='Lista de Fluxogramas'),
    path('flow/bsi/opcionais', views.flow_bsi_op, name='Fluxograma BSI - Opcionais'),
    path('flow/bsi-1b-h/', views.flow_bsi_1b_h, name='Fluxograma BSI - 01B - Horizontal'),

    path('flow/cont/', views.flow_cont, name='flow_cont'),
    path('flow/cont/opcionais', views.flow_cont_op, name='flow_cont_op'),

    path('flow/dir/', views.flow_dir, name='flow_dir'),
    path('flow/dir/opcionais', views.flow_dir_op, name='flow_dir_op'),

    path('flow/ped-h/', views.flow_ped_h, name='flow_ped_h'),
    path('flow/ped/opcionais', views.flow_ped_op, name='Fluxograma Pedagogia - Opcionais'),

    path('flow/let-esp/', views.flow_let_esp, name='flow_let_esp'),
    path('flow/let-esp/opcionais', views.flow_let_esp_op, name='flow_let_esp_op'),

    path('flow/let-por/', views.flow_let_por, name='flow_let_por'),
    path('flow/let-por/opcionais', views.flow_let_por_op, name='flow_let_por_op'),

    path('flow/let-ing/', views.flow_let_ing, name='flow_let_ing'),
    path('flow/let-ing/opcionais', views.flow_let_ing_op, name='flow_let_ing_op'),

    path('flow/mat-h/', views.flow_mat_h, name='flow_mat_h'),
    path('flow/mat/opcionais', views.flow_mat_op, name='flow_mat_op'),

    path('flow/adm/', views.flow_adm, name='flow_adm'),
    path('flow/adm/opcionais', views.flow_adm_op, name='flow_adm_op'),

    path('flow/tur/', views.flow_tur, name='flow_tur'),
    path('flow/tur/opcionais', views.flow_tur_op, name='flow_tur_op'),

    path('turmas/', views.turmas_list, name='turmas_list'),
    path('turmas/cont', views.turmas_cont, name='turmas_contabeis'),
    path('turmas/dir', views.turmas_dir, name='turmas_direito'),
    path('turmas/mat', views.turmas_mat, name='turmas_matemática'),
    path('turmas/bsi', views.turmas_bsi, name='turmas_sistemas'),
    path('turmas/ped', views.turmas_ped, name='turmas_pedagogia'),
    path('turmas/adm', views.turmas_adm, name='turmas_administracao'),
    path('turmas/tur', views.turmas_tur, name='turmas_turismo'),
    path('turmas/let-esp', views.turmas_let_esp, name='turmas_letras_esp'),
    path('turmas/let-por', views.turmas_let_por, name='turmas_letras_por'),
    path('turmas/let-ing', views.turmas_let_ing, name='turmas_letras_ing'),
    path('turmas/<int:pk>/', views.TurmaDetailView.as_view(), name='turma_detalhar'),

    path('sugestao/', views.sugestao_list, name='sugestao_list'),
    path('sugestao/<int:pk>/', views.SugestaoTurmaDetailView.as_view(), name='sugestao_detalhar'),
    path('ajax/load-docentes/', suggest_view.load_docentes, name='ajax_load_docentes'),
    path('ajax/check_vinculo_docente/', suggest_view.check_vinculo_docente, name='ajax_check_vinculo_docente'),
    path('ajax/load-vinculos/', suggest_view.load_vinculos, name='ajax_load_vinculos'),

    path('solicitacao/<int:pk>/', views.sugestao_solicitar, name='sugestao_solicitar'),
    path('solicitacao/listar/<int:pk>/', views.solicitacao_turma_listar, name='solicitacao_turma_listar'),
    path('solicitacao/deletar/<int:pk>/', views.solicitacao_deletar, name='solicitacao_deletar'),

    path('sugestao/adm/list', views.sugestao_adm_list, name='sugestao_adm_list'),
    path('sugestao/adm/manter', views.sugestao_adm_manter, name='sugestao_adm_manter'),
    path('sugestao/adm/incluir', views.sugestao_adm_incluir, name='sugestao_adm_incluir'),
    path('sugestao/adm/editar/<int:pk>/', views.sugestao_adm_editar, name='sugestao_adm_editar'),
    path('sugestao/adm/deletar/<int:pk>/', views.sugestao_adm_deletar, name='sugestao_adm_deletar'),

    path('sugestao/cont/list', sugestao_cont_list, name='sugestao_cont_list'),
    path('sugestao/cont/manter', sugestao_cont_manter, name='sugestao_cont_manter'),
    path('sugestao/cont/incluir', sugestao_cont_incluir, name='sugestao_cont_incluir'),
    path('sugestao/cont/editar/<int:pk>/', sugestao_cont_editar, name='sugestao_cont_editar'),
    path('sugestao/cont/deletar/<int:pk>/', sugestao_cont_deletar, name='sugestao_cont_deletar'),

    path('sugestao/dir/list', views.sugestao_dir_list, name='sugestao_dir_list'),
    path('sugestao/dir/manter', views.sugestao_dir_manter, name='sugestao_dir_manter'),
    path('sugestao/dir/incluir', views.sugestao_dir_incluir, name='sugestao_dir_incluir'),
    path('sugestao/dir/editar/<int:pk>/', views.sugestao_dir_editar, name='sugestao_dir_editar'),
    path('sugestao/dir/deletar/<int:pk>/', views.sugestao_dir_deletar, name='sugestao_dir_deletar'),

    path('sugestao/let-esp/list', sugestao_letras_view.sugestao_let_esp_list, name='sugestao_let_esp_list'),
    path('sugestao/let-esp/manter', sugestao_letras_view.sugestao_let_esp_manter, name='sugestao_let_esp_manter'),
    path('sugestao/let-esp/incluir', sugestao_letras_view.sugestao_let_esp_incluir, name='sugestao_let_esp_incluir'),
    path('sugestao/let-esp/editar/<int:pk>/', sugestao_letras_view.sugestao_let_esp_editar,
         name='sugestao_let_esp_editar'),
    path('sugestao/let-esp/deletar/<int:pk>/', sugestao_letras_view.sugestao_let_esp_deletar,
         name='sugestao_let_esp_deletar'),

    path('sugestao/let-por/list', sugestao_letras_view.sugestao_let_por_list, name='sugestao_let_por_list'),
    path('sugestao/let-por/manter', sugestao_letras_view.sugestao_let_por_manter, name='sugestao_let_por_manter'),
    path('sugestao/let-por/incluir', sugestao_letras_view.sugestao_let_por_incluir, name='sugestao_let_por_incluir'),
    path('sugestao/let-por/editar/<int:pk>/', sugestao_letras_view.sugestao_let_por_editar,
         name='sugestao_let_por_editar'),
    path('sugestao/let-por/deletar/<int:pk>/', sugestao_letras_view.sugestao_let_por_deletar,
         name='sugestao_let_por_deletar'),

    path('sugestao/let-ing/list', sugestao_letras_view.sugestao_let_ing_list, name='sugestao_let_ing_list'),
    path('sugestao/let-ing/manter', sugestao_letras_view.sugestao_let_ing_manter, name='sugestao_let_ing_manter'),
    path('sugestao/let-ing/incluir', sugestao_letras_view.sugestao_let_ing_incluir, name='sugestao_let_ing_incluir'),
    path('sugestao/let-ing/editar/<int:pk>/', sugestao_letras_view.sugestao_let_ing_editar,
         name='sugestao_let_ing_editar'),
    path('sugestao/let-ing/deletar/<int:pk>/', sugestao_letras_view.sugestao_let_ing_deletar,
         name='sugestao_let_ing_deletar'),

    path('sugestao/mat/list', views.sugestao_mat_list, name='sugestao_mat_list'),
    path('sugestao/mat/manter', views.sugestao_mat_manter, name='sugestao_mat_manter'),
    path('sugestao/mat/incluir', views.sugestao_mat_incluir, name='sugestao_mat_incluir'),
    path('sugestao/mat/editar/<int:pk>/', views.sugestao_mat_editar, name='sugestao_mat_editar'),
    path('sugestao/mat/deletar/<int:pk>/', views.sugestao_mat_deletar, name='sugestao_mat_deletar'),

    path('sugestao/bsi/list', views.sugestao_bsi_list, name='sugestao_bsi_list'),
    path('sugestao/bsi/manter', views.sugestao_bsi_manter, name='sugestao_bsi_manter'),
    path('sugestao/bsi/incluir', views.sugestao_bsi_incluir, name='sugestao_bsi_incluir'),
    path('sugestao/bsi/editar/<int:pk>/', views.sugestao_bsi_editar, name='sugestao_bsi_editar'),
    path('sugestao/bsi/deletar/<int:pk>/', views.sugestao_bsi_deletar, name='sugestao_bsi_deletar'),

    path('sugestao/ped/list', views.sugestao_ped_list, name='sugestao_ped_list'),
    path('sugestao/ped/manter', views.sugestao_ped_manter, name='sugestao_ped_manter'),
    path('sugestao/ped/incluir', views.sugestao_ped_incluir, name='sugestao_ped_incluir'),
    path('sugestao/ped/editar/<int:pk>/', views.sugestao_ped_editar, name='sugestao_ped_editar'),
    path('sugestao/ped/deletar/<int:pk>/', views.sugestao_ped_deletar, name='sugestao_ped_deletar'),

    path('sugestao/tur/list', views.sugestao_tur_list, name='sugestao_tur_list'),
    path('sugestao/tur/manter', views.sugestao_tur_manter, name='sugestao_tur_manter'),
    path('sugestao/tur/incluir', views.sugestao_tur_incluir, name='sugestao_tur_incluir'),
    path('sugestao/tur/editar/<int:pk>/', views.sugestao_tur_editar, name='sugestao_tur_editar'),
    path('sugestao/tur/deletar/<int:pk>/', views.sugestao_tur_deletar, name='sugestao_tur_deletar'),

    path('plot/', views.plot, name='Plot de Gráfico')
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
