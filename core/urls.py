from django.conf.global_settings import STATIC_ROOT
from django.conf.urls.static import static
from django.urls import path

from mysite.settings import STATIC_URL, MEDIA_URL, MEDIA_ROOT, DEBUG
from . import views

urlpatterns = [
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
    path('docente/list/', views.docente_list, name='Lista de Docentes'),
    path('docente/<int:pk>/', views.DocenteDetailView.as_view(), name='docente_detalhar'),

    path('sala/list/', views.sala_list, name='Lista de Salas'),
    path('flow/', views.flow_list, name='Lista de Fluxogramas'),
    path('flow/bsi/', views.flow_bsi, name='Fluxograma BSI'),
    path('flow/bsi/opcionais', views.flow_bsi_op, name='Fluxograma BSI - Opcionais'),
    path('flow/bsi-1b/', views.flow_bsi_1b, name='Fluxograma BSI - 01B'),
    path('flow/bsi-1b-h/', views.flow_bsi_1b_h, name='Fluxograma BSI - 01B - Horizontal'),

    path('flow/ped/', views.flow_ped, name='Fluxograma Pedagogia'),
    path('flow/ped-h/', views.flow_ped_h, name='flow_ped_h'),
    path('flow/ped/opcionais', views.flow_ped_op, name='Fluxograma Pedagogia - Opcionais'),

    path('flow/mat-h/', views.flow_mat_h, name='flow_mat_h'),
    path('flow/mat/opcionais', views.flow_mat_op, name='flow_mat_op'),

    path('usuario/cadastrar', views.cadastrar_usuario, name='Cadastro de Usuário'),
    path('usuario/logar', views.logar_usuario, name='Login de Usuário'),
    path('usuario/deslogar', views.deslogar_usuario, name='Logout de Usuário'),
    path('usuario/alterar_senha', views.alterar_senha, name='Alterar Senha de Usuário'),

    path('turma/', views.turma_list, name='Lista de Turmas por Curso'),
    path('turma/mat', views.turma_mat, name='Turmas de Matemática'),
    path('turma/bsi', views.turma_bsi, name='Turmas de Sistemas de Informação'),
    path('turma/ped', views.turma_ped, name='Turmas de Pedagogia'),
    path('turma/<int:pk>/', views.TurmaDetailView.as_view(), name='turma_detalhar'),

    path('sugestao/', views.sugestao_list, name='sugestao_list'),
    path('sugestao/<int:pk>/', views.SugestaoTurmaDetailView.as_view(), name='sugestao_detalhar'),
    # path('sugestao/edit/<int:pk>/', views.edit, name='sugestao_edit'),
    path('sugestao/delete/<int:pk>/', views.sugestao_deletar, name='sugestao_delete'),

    path('sugestao/mat/list', views.sugestao_mat_list, name='sugestao_mat_list'),
    path('sugestao/mat/manter', views.sugestao_mat_manter, name='sugestao_mat_manter'),
    path('sugestao/mat/incluir', views.sugestao_mat_incluir, name='sugestao_mat_incluir'),
    path('sugestao/mat/editar/<int:pk>/', views.sugestao_mat_editar, name='sugestao_mat_editar'),

    path('sugestao/bsi/list', views.sugestao_bsi_list, name='sugestao_bsi_list'),
    path('sugestao/bsi/manter', views.sugestao_bsi_manter, name='sugestao_bsi_manter'),
    path('sugestao/bsi/incluir', views.sugestao_bsi_incluir, name='sugestao_bsi_incluir'),
    path('sugestao/bsi/editar/<int:pk>/', views.sugestao_bsi_editar, name='sugestao_bsi_editar'),

    path('sugestao/ped/list', views.sugestao_ped_list, name='sugestao_ped_list'),
    path('sugestao/ped/manter', views.sugestao_ped_manter, name='sugestao_ped_manter'),
    path('sugestao/ped/incluir', views.sugestao_ped_incluir, name='sugestao_ped_incluir'),
    path('sugestao/ped/editar/<int:pk>/', views.sugestao_ped_editar, name='sugestao_ped_editar'),

    path('plot/', views.plot, name='Plot de Gráfico')
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
