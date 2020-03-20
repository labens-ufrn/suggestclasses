from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.list, name='list'),
    path('<int:horario_id>/', views.detail, name='detail'),
    path('curso/<int:curso_id>/', views.curso_detail, name='curso_detail'),
    path('curso/list/', views.curso_list, name='Lista de Cursos'),
    path('departamento/list/', views.departamento_list, name='Lista de Departamentos'),
    path('componente/list/', views.componente_list, name='Lista de Componentes Curriculares'),
    path('curriculo/list/', views.curriculo_list, name='Lista de Estruturas Curriculares'),
    path('flow/', views.flow_list, name='Lista de Fluxogramas'),
    path('flow/bsi/', views.flow_bsi, name='Fluxograma BSI'),
    path('flow/bsi/opcionais', views.flow_bsi_op, name='Fluxograma BSI - Opcionais'),
    path('flow/bsi-1b/', views.flow_bsi_1b, name='Fluxograma BSI - 01B'),
    path('flow/ped/', views.flow_ped, name='Fluxograma Pedagogia'),
    path('usuario/cadastrar', views.cadastrar_usuario, name='Cadastro de Usuário'),
    path('usuario/logar', views.logar_usuario, name='Login de Usuário'),
    path('usuario/deslogar', views.deslogar_usuario, name='Logout de Usuário'),
    path('usuario/alterar_senha', views.alterar_senha, name='Alterar Senha de Usuário'),
    path('turma/', views.turma_list, name='Lista de Turmas por Curso'),
    path('turma/bsi', views.turma_bsi, name='Turmas de Sistemas de Informação'),
    path('turma/ped', views.turma_ped, name='Turmas de Pedagogia'),
    path('plot/', views.plot, name='Plot de Gráfico'),
]
