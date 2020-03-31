from django.conf.global_settings import STATIC_ROOT
from django.conf.urls.static import static
from django.urls import path

from mysite.settings import STATIC_URL, MEDIA_URL, MEDIA_ROOT, DEBUG
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('horarios_list/', views.horarios_list, name='horarios_list'),
    path('<int:horario_id>/', views.detail, name='detail'),
    path('curso/<int:curso_id>/', views.curso_detail, name='curso_detail'),
    path('curso/list/', views.curso_list, name='Lista de Cursos'),
    path('departamento/list/', views.departamento_list, name='Lista de Departamentos'),
    path('componente/list/', views.componente_list, name='Lista de Componentes Curriculares'),
    path('curriculo/list/', views.curriculo_list, name='Lista de Estruturas Curriculares'),
    path('docente/list/', views.docente_list, name='Lista de Docentes'),
    path('sala/list/', views.sala_list, name='Lista de Salas'),
    path('flow/', views.flow_list, name='Lista de Fluxogramas'),
    path('flow/bsi/', views.flow_bsi, name='Fluxograma BSI'),
    path('flow/bsi/opcionais', views.flow_bsi_op, name='Fluxograma BSI - Opcionais'),
    path('flow/bsi-1b/', views.flow_bsi_1b, name='Fluxograma BSI - 01B'),
    path('flow/ped/', views.flow_ped, name='Fluxograma Pedagogia'),
    path('flow/ped/opcionais', views.flow_ped_op, name='Fluxograma Pedagogia - Opcionais'),
    path('usuario/cadastrar', views.cadastrar_usuario, name='Cadastro de Usuário'),
    path('usuario/logar', views.logar_usuario, name='Login de Usuário'),
    path('usuario/deslogar', views.deslogar_usuario, name='Logout de Usuário'),
    path('usuario/alterar_senha', views.alterar_senha, name='Alterar Senha de Usuário'),
    path('turma/', views.turma_list, name='Lista de Turmas por Curso'),
    path('turma/bsi', views.turma_bsi, name='Turmas de Sistemas de Informação'),
    path('turma/ped', views.turma_ped, name='Turmas de Pedagogia'),
    path('sugestao/', views.sugestao_list, name='Lista de Sugestão de Turmas por Curso'),
    path('sugestao/bsi/incluir', views.sugestao_bsi_incluir, name='Incluir Sugestão de Turmas Sistemas de Informação'),
    path('sugestao/bsi/list', views.sugestao_bsi, name='Listar Sugestão de Turmas de Sistemas de Informação'),
    path('sugestao/bsi/manter', views.sugestao_bsi_manter, name='Manter Sugestão de Turmas de Sistemas de Informação'),
    path('sugestao/ped/list', views.sugestao_ped, name='Sugestão de Turmas de Pedagogia'),
    path('plot/', views.plot, name='Plot de Gráfico'),
    path('sugestao/index', views.IndexView.as_view(), name='sugestao_index'),
    path('sugestao/<int:pk>/', views.SugestaoTurmaDetailView.as_view(), name='sugestao_detail'),
    path('sugestao/edit/<int:pk>/', views.edit, name='sugestao_edit'),
    path('sugestao/create/', views.create, name='sugestao_create'),
    path('sugestao/delete/<int:pk>/', views.delete, name='sugestao_delete')
]

if DEBUG:
    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
