from django.conf.global_settings import STATIC_ROOT
from django.conf.urls.static import static
from django.urls import path

from mysite.settings import STATIC_URL, MEDIA_URL, MEDIA_ROOT, DEBUG
from . import views
from .visoes import suggest_view

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

    path('flow/', views.flow_list, name='Lista de Fluxogramas'),
    path('flow/bsi/', views.flow_bsi, name='Fluxograma BSI'),
    path('flow/bsi/opcionais', views.flow_bsi_op, name='Fluxograma BSI - Opcionais'),
    path('flow/bsi-1b/', views.flow_bsi_1b, name='Fluxograma BSI - 01B'),
    path('flow/bsi-1b-h/', views.flow_bsi_1b_h, name='Fluxograma BSI - 01B - Horizontal'),

    path('flow/dir/', views.flow_dir, name='flow_dir'),
    path('flow/dir/opcionais', views.flow_dir_op, name='flow_dir_op'),

    path('flow/ped-h/', views.flow_ped_h, name='flow_ped_h'),
    path('flow/ped/opcionais', views.flow_ped_op, name='Fluxograma Pedagogia - Opcionais'),

    path('flow/mat-h/', views.flow_mat_h, name='flow_mat_h'),
    path('flow/mat/opcionais', views.flow_mat_op, name='flow_mat_op'),

    path('turmas/', views.turmas_list, name='turmas_list'),
    path('turmas/dir', views.turmas_dir, name='turmas_direito'),
    path('turmas/mat', views.turmas_mat, name='turmas_matemática'),
    path('turmas/bsi', views.turmas_bsi, name='turmas_sistemas'),
    path('turmas/ped', views.turmas_ped, name='turmas_pedagogia'),
    path('turmas/<int:pk>/', views.TurmaDetailView.as_view(), name='turma_detalhar'),

    path('sugestao/', views.sugestao_list, name='sugestao_list'),
    path('sugestao/<int:pk>/', views.SugestaoTurmaDetailView.as_view(), name='sugestao_detalhar'),
    path('ajax/load-docentes/', suggest_view.load_docentes, name='ajax_load_docentes'),
    path('ajax/check_vinculo_docente/', suggest_view.check_vinculo_docente, name='ajax_check_vinculo_docente'),
    path('ajax/load-vinculos/', suggest_view.load_vinculos, name='ajax_load_vinculos'),

    path('solicitacao/<int:pk>/', views.sugestao_solicitar, name='sugestao_solicitar'),
    path('solicitacao/listar/<int:pk>/', views.solicitacao_turma_listar, name='solicitacao_turma_listar'),
    path('solicitacao/deletar/<int:pk>/', views.solicitacao_deletar, name='solicitacao_deletar'),

    path('sugestao/dir/list', views.sugestao_dir_list, name='sugestao_dir_list'),
    path('sugestao/dir/manter', views.sugestao_dir_manter, name='sugestao_dir_manter'),
    path('sugestao/dir/incluir', views.sugestao_dir_incluir, name='sugestao_dir_incluir'),
    path('sugestao/dir/editar/<int:pk>/', views.sugestao_dir_editar, name='sugestao_dir_editar'),
    path('sugestao/dir/deletar/<int:pk>/', views.sugestao_dir_deletar, name='sugestao_dir_deletar'),

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

    path('plot/', views.plot, name='Plot de Gráfico')
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
