import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()
from django.contrib.auth.models import User
from dateutil.parser import parse
from core.models import Centro, Departamento, ComponenteCurricular, Docente, EstruturaCurricular, Curso, \
    OrganizacaoCurricular, Turma, Sala, SugestaoTurma, Discente


def criar_dados():
    print("Povoando Dados para Testes ...")

    criar_usuario()
    criar_centro()
    criar_salas()
    criar_departamentos()
    criar_docentes()
    criar_cursos()
    criar_componentes()
    criar_estruturas()
    criar_curriculos()
    criar_turmas()
    criar_sugestoes_turmas()
    criar_discentes()


def remover_dados():
    print("Removendo Dados dos Testes ...")
    remover_discentes()
    remover_sugestoes_turmas()
    remover_turmas()
    remover_curriculos()
    remover_estruturas()
    remover_componentes()
    remover_cursos()
    remover_docentes()
    remover_departamentos()
    remover_salas()
    remover_centro()
    remover_usuario()


def criar_usuario():
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    user.last_name = 'Lennon'
    user.save()


def criar_discentes():
    Discente.objects.create(matricula='20209876543', nome_discente='Zé Silva', sexo='M',
                            ano_ingresso=2020, periodo_ingresso=1,
                            forma_ingresso='SiSU', tipo_discente='REGULAR', status='ATIVO',
                            sigla_nivel_ensino='G', nivel_ensino='GRADUAÇÃO',
                            id_curso='7191770', nome_curso='SISTEMAS DE INFORMAÇÃO',
                            modalidade_educacao='PRESENCIAL',
                            id_unidade=1482, nome_unidade='CENTRO DE  ENSINO SUPERIOR DO SERIDÓ',
                            id_unidade_gestora=1482, nome_unidade_gestora='CENTRO DE  ENSINO SUPERIOR DO SERIDÓ')


def criar_centro():
    Centro.objects.create(id_unidade=9999, codigo=9999, nome='Centro de Teste',
                          sigla='CTESTE', endereco='Rua Joaquim Gregório, Penedo, Caicó - RN',
                          site='https://www.ceres.ufrn.br/')


def remover_centro():
    try:
        Centro.objects.get(id_unidade=9999).delete()
    except Centro.DoesNotExist:
        print('Centro não Existe!')


def remover_usuario():
    try:
        User.objects.get(username='john').delete()
    except User.DoesNotExist:
        print('Usuário não Existe!')


def remover_discentes():
    try:
        Discente.objects.get(matricula=20209876543).delete()
    except Discente.DoesNotExist:
        print('Discente não Existe!')


def criar_salas():
    centro = Centro.objects.get(id_unidade=9999)
    Sala.objects.create(nome='Sala A01', sigla='A01', capacidade=25, tamanho=None, bloco='Bloco A',
                        centro=centro, campus='Campus Caicó')


def remover_salas():
    try:
        Sala.objects.get(sigla='A01', bloco='Bloco A', centro__id_unidade=9999).delete()
    except Sala.DoesNotExist:
        print('Sala não Existe!')


def criar_departamentos():
    centro = Centro.objects.get(id_unidade=9999)
    Departamento.objects.create(id_unidade=9998, codigo=9998, nome='Departamento de Teste', sigla='DTS',
                                endereco='Rua Joaquim Gregório, Penedo, Caicó - RN',
                                centro=centro)


def remover_departamentos():
    try:
        Departamento.objects.get(id_unidade=9998).delete()
    except Departamento.DoesNotExist:
        print('Departamento não Existe!')


def criar_docentes():
    departamento = Departamento.objects.get(id_unidade=9998)
    Docente.objects.create(siape=9999999, nome='Nome Docente Teste 1', sexo='M', formacao='Mestrado',
                           tipo_jornada_trabalho='Dedicação Exclusiva', vinculo='Ativo Permanente',
                           categoria='PROFESSOR DO MAGISTERIO SUPERIOR', classe_funcional='Classe C - Adjunto',
                           id_unidade_lotacao=departamento.id_unidade,
                           lotacao='Departamento de Teste', admissao=parse('2020/03/30'))
    Docente.objects.create(siape=9999997, nome='Nome Docente Teste 2', sexo='F', formacao='Doutorado',
                           tipo_jornada_trabalho='Dedicação Exclusiva', vinculo='Ativo Permanente',
                           categoria='PROFESSOR DO MAGISTERIO SUPERIOR', classe_funcional='Classe D - Adjunto',
                           id_unidade_lotacao=departamento.id_unidade,
                           lotacao='Departamento de Teste', admissao=parse('2020/03/30'))


def remover_docentes():
    try:
        Docente.objects.get(siape=9999999).delete()
        Docente.objects.get(siape=9999998).delete()
    except Docente.DoesNotExist:
        print('Docente não Existe!')


def criar_cursos():
    centro = Centro.objects.get(id_unidade=9999)
    docente1 = Docente.objects.get(siape=9999999)
    docente2 = Docente.objects.get(siape=9999997)
    Curso.objects.create(codigo=9999, nome='Sistemas de Informação', coordenador=docente1, nivel='Graduação',
                         grau='Bacharelado', modalidade='Presencial', turno='Matutino e Vespertino',
                         centro=centro)
    Curso.objects.create(codigo=9998, nome='Curso Pedagogia', coordenador=docente2, nivel='Graduação',
                         grau='Licenciatura', modalidade='Presencial', turno='Matutino e Vespertino',
                         centro=centro)


def remover_cursos():
    try:
        Curso.objects.get(codigo=9999).delete()
        Curso.objects.get(codigo=9998).delete()
    except Curso.DoesNotExist:
        print('Curso não Existe!')


def criar_componentes():
    departamento = Departamento.objects.get(id_unidade=9998)
    ComponenteCurricular.objects.create(id_componente=99999, tipo='DISCIPLINA',
                                        codigo='DCT9999', nivel='G', nome='BANCO DE DADOS',
                                        ch_teorica=30, ch_pratica=30, ch_estagio=0,
                                        ch_total=60, ch_docente=60, ch_ead=0,
                                        cr_max_ead=0, equivalencia='( BSI2201 )',
                                        requisito='( ( BSI1106 ) OU ( DCT1106 ) )', corequisito='',
                                        ementa='ementa', modalidade='Presencial', departamento=departamento)
    ComponenteCurricular.objects.create(id_componente=99998, tipo='DISCIPLINA',
                                        codigo='DCT9998', nivel='G', nome='ENGENHARIA DE SOFTWARE',
                                        ch_teorica=30, ch_pratica=30, ch_estagio=0,
                                        ch_total=60, ch_docente=60, ch_ead=0,
                                        cr_max_ead=0, equivalencia='( BSI2301 )',
                                        requisito='( ( BSI1106 ) OU ( DCT1106 ) )', corequisito='',
                                        ementa='ementa', modalidade='Presencial', departamento=departamento)
    ComponenteCurricular.objects.create(id_componente=99997, tipo='DISCIPLINA',
                                        codigo='DCT9997', nivel='G', nome='TESTE DE SOFTWARE',
                                        ch_teorica=30, ch_pratica=30, ch_estagio=0,
                                        ch_total=60, ch_docente=60, ch_ead=0,
                                        cr_max_ead=0, equivalencia='( BSI2201 )',
                                        requisito='( ( BSI1106 ) OU ( DCT1106 ) )', corequisito='',
                                        ementa='ementa', modalidade='Presencial', departamento=departamento)
    ComponenteCurricular.objects.create(id_componente=99996, tipo='DISCIPLINA',
                                        codigo='DCT9996', nivel='G', nome='PROGRAMAÇÃO WEB',
                                        ch_teorica=30, ch_pratica=30, ch_estagio=0,
                                        ch_total=60, ch_docente=60, ch_ead=0,
                                        cr_max_ead=0, equivalencia='( BSI2201 )',
                                        requisito='( ( BSI1106 ) OU ( DCT1106 ) )', corequisito='',
                                        ementa='ementa', modalidade='Presencial', departamento=departamento)


def remover_componentes():
    try:
        ComponenteCurricular.objects.get(id_componente=99999).delete()
        ComponenteCurricular.objects.get(id_componente=99998).delete()
        ComponenteCurricular.objects.get(id_componente=99997).delete()
        ComponenteCurricular.objects.get(id_componente=99996).delete()
    except ComponenteCurricular.DoesNotExist:
        print('ComponenteCurricular não Existe!')


def criar_estruturas():
    curso1 = Curso.objects.get(codigo=9999)
    curso2 = Curso.objects.get(codigo=9998)
    EstruturaCurricular.objects.create(id_curriculo=999999999, codigo='01',
                                       nome='Sistemas de Informação - CAICÓ - MT - BACHARELADO',
                                       semestre_conclusao_minimo=8, semestre_conclusao_ideal=8,
                                       semestre_conclusao_maximo=12, meses_conclusao_minimo=None,
                                       meses_conclusao_ideal=None, meses_conclusao_maximo=None, cr_total_minimo=148,
                                       ch_total_minima=3000, ch_optativas_minima=300, ch_complementar_minima=180,
                                       max_eletivos=240, ch_nao_atividade_obrigatoria=2220,
                                       cr_nao_atividade_obrigatorio=148, ch_atividade_obrigatoria=480,
                                       cr_minimo_semestre=8, cr_ideal_semestre=24, cr_maximo_semestre=28,
                                       ch_minima_semestre=120, ch_ideal_semestre=None, ch_maxima_semestre=0,
                                       periodo_entrada_vigor=1, ano_entrada_vigor=2020,
                                       observacao='', curso=curso1)

    EstruturaCurricular.objects.create(id_curriculo=999999998, codigo='01',
                                       nome='Pedagogia - CAICÓ - MT - LICENCIATURA',
                                       semestre_conclusao_minimo=8, semestre_conclusao_ideal=8,
                                       semestre_conclusao_maximo=12, meses_conclusao_minimo=None,
                                       meses_conclusao_ideal=None, meses_conclusao_maximo=None, cr_total_minimo=148,
                                       ch_total_minima=3000, ch_optativas_minima=300, ch_complementar_minima=180,
                                       max_eletivos=240, ch_nao_atividade_obrigatoria=2220,
                                       cr_nao_atividade_obrigatorio=148, ch_atividade_obrigatoria=480,
                                       cr_minimo_semestre=8, cr_ideal_semestre=24, cr_maximo_semestre=28,
                                       ch_minima_semestre=120, ch_ideal_semestre=None, ch_maxima_semestre=0,
                                       periodo_entrada_vigor=1, ano_entrada_vigor=2020,
                                       observacao='', curso=curso2)


def remover_estruturas():
    try:
        EstruturaCurricular.objects.get(id_curriculo=999999999).delete()
        EstruturaCurricular.objects.get(id_curriculo=999999998).delete()
    except EstruturaCurricular.DoesNotExist:
        print('EstruturaCurricular não Existe!')


def criar_curriculos():
    estrutura1 = EstruturaCurricular.objects.get(id_curriculo=999999999)
    estrutura2 = EstruturaCurricular.objects.get(id_curriculo=999999998)
    componente1 = ComponenteCurricular.objects.get(id_componente=99999)
    componente2 = ComponenteCurricular.objects.get(id_componente=99998)
    componente3 = ComponenteCurricular.objects.get(id_componente=99997)
    componente4 = ComponenteCurricular.objects.get(id_componente=99996)
    OrganizacaoCurricular.objects.create(id_curriculo_componente=999999, estrutura=estrutura1,
                                         componente=componente1, semestre=1, tipo_vinculo='OBRIGATÓRIO',
                                         nivel='GRADUAÇÃO')
    OrganizacaoCurricular.objects.create(id_curriculo_componente=999998, estrutura=estrutura1,
                                         componente=componente2, semestre=1, tipo_vinculo='OBRIGATÓRIO',
                                         nivel='GRADUAÇÃO')
    OrganizacaoCurricular.objects.create(id_curriculo_componente=999997, estrutura=estrutura1,
                                         componente=componente3, semestre=2, tipo_vinculo='OBRIGATÓRIO',
                                         nivel='GRADUAÇÃO')

    OrganizacaoCurricular.objects.create(id_curriculo_componente=999996, estrutura=estrutura2,
                                         componente=componente2, semestre=1, tipo_vinculo='OBRIGATÓRIO',
                                         nivel='GRADUAÇÃO')
    OrganizacaoCurricular.objects.create(id_curriculo_componente=999995, estrutura=estrutura2,
                                         componente=componente4, semestre=2, tipo_vinculo='OPTATIVO',
                                         nivel='GRADUAÇÃO')


def remover_curriculos():
    try:
        OrganizacaoCurricular.objects.get(id_curriculo_componente=999999).delete()
        OrganizacaoCurricular.objects.get(id_curriculo_componente=999998).delete()
        OrganizacaoCurricular.objects.get(id_curriculo_componente=999997).delete()
        OrganizacaoCurricular.objects.get(id_curriculo_componente=999996).delete()
        OrganizacaoCurricular.objects.get(id_curriculo_componente=999995).delete()
    except OrganizacaoCurricular.DoesNotExist:
        print('OrganizacaoCurricular não Existe!')


def criar_turmas():
    docente1 = Docente.objects.get(siape=9999999)
    docente2 = Docente.objects.get(siape=9999997)
    componente1 = ComponenteCurricular.objects.get(id_componente=99999)
    componente2 = ComponenteCurricular.objects.get(id_componente=99998)
    componente3 = ComponenteCurricular.objects.get(id_componente=99997)
    sala = Sala.objects.get(sigla='A01', bloco='Bloco A', centro__id_unidade=9999)

    Turma.objects.create(id_turma=99999999, codigo_turma='01', docente=docente1, matricula_docente_externo=None,
                         observacao='', componente=componente1, ch_dedicada_periodo=60,
                         nivel_ensino='GRADUAÇÃO', campus_turma=sala.campus, local=sala, ano=2020,
                         periodo=1, data_inicio=parse('2020/03/30'), data_fim=parse('2020/07/30'),
                         descricao_horario='24T12', total_solicitacoes=15, capacidade_aluno=25, tipo='REGULAR',
                         distancia=False, data_consolidacao=None, agrupadora=False, id_turma_agrupadora=None,
                         qtd_aulas_lancadas=5, situacao_turma='ABERTA', convenio=None,
                         modalidade_participantes='Presencial')

    Turma.objects.create(id_turma=99999998, codigo_turma='01', docente=docente2, matricula_docente_externo=None,
                         observacao='', componente=componente2, ch_dedicada_periodo=60,
                         nivel_ensino='GRADUAÇÃO', campus_turma=sala.campus, local=sala, ano=2020,
                         periodo=1, data_inicio=parse('2020/03/30'), data_fim=parse('2020/07/30'),
                         descricao_horario='24T34', total_solicitacoes=20, capacidade_aluno=25, tipo='REGULAR',
                         distancia=False, data_consolidacao=None, agrupadora=False, id_turma_agrupadora=None,
                         qtd_aulas_lancadas=5, situacao_turma='ABERTA', convenio=None,
                         modalidade_participantes='Presencial')

    Turma.objects.create(id_turma=99999997, codigo_turma='01', docente=docente1, matricula_docente_externo=None,
                         observacao='', componente=componente3, ch_dedicada_periodo=60,
                         nivel_ensino='GRADUAÇÃO', campus_turma=sala.campus, local=sala, ano=2020,
                         periodo=1, data_inicio=parse('2020/03/30'), data_fim=parse('2020/07/30'),
                         descricao_horario='35T12', total_solicitacoes=15, capacidade_aluno=25, tipo='REGULAR',
                         distancia=False, data_consolidacao=None, agrupadora=False, id_turma_agrupadora=None,
                         qtd_aulas_lancadas=5, situacao_turma='ABERTA', convenio=None,
                         modalidade_participantes='Presencial')

    Turma.objects.create(id_turma=99999996, codigo_turma='02', docente=docente2, matricula_docente_externo=None,
                         observacao='', componente=componente3, ch_dedicada_periodo=60,
                         nivel_ensino='GRADUAÇÃO', campus_turma=sala.campus, local=sala, ano=2020,
                         periodo=1, data_inicio=parse('2020/03/30'), data_fim=parse('2020/07/30'),
                         descricao_horario='35T34', total_solicitacoes=15, capacidade_aluno=25, tipo='REGULAR',
                         distancia=False, data_consolidacao=None, agrupadora=False, id_turma_agrupadora=None,
                         qtd_aulas_lancadas=5, situacao_turma='ABERTA', convenio=None,
                         modalidade_participantes='Presencial')
    print(Turma.objects.filter(id_turma=99999996))


def remover_turmas():
    try:
        Turma.objects.get(id_turma=99999999).delete()
        Turma.objects.get(id_turma=99999998).delete()
        Turma.objects.get(id_turma=99999997).delete()
        Turma.objects.get(id_turma=99999996).delete()
    except Turma.DoesNotExist:
        print('Turma não Existe!')


def criar_sugestoes_turmas():
    docente1 = Docente.objects.get(siape=9999999)
    docente2 = Docente.objects.get(siape=9999997)
    componente1 = ComponenteCurricular.objects.get(id_componente=99999)
    componente2 = ComponenteCurricular.objects.get(id_componente=99998)
    componente3 = ComponenteCurricular.objects.get(id_componente=99997)
    sala = Sala.objects.get(sigla='A01', bloco='Bloco A', centro__id_unidade=9999)

    SugestaoTurma.objects.create(codigo_turma='01', docente=docente1, matricula_docente_externo=None,
                                 componente=componente1, campus_turma=sala.campus, local=sala, ano=2020,
                                 periodo=2, descricao_horario='24T12', capacidade_aluno=25, tipo='REGULAR')

    SugestaoTurma.objects.create(codigo_turma='01', docente=docente2, matricula_docente_externo=None,
                                 componente=componente2, campus_turma=sala.campus, local=sala, ano=2020,
                                 periodo=2, descricao_horario='24T34', capacidade_aluno=25, tipo='REGULAR')

    SugestaoTurma.objects.create(codigo_turma='01', docente=docente1, matricula_docente_externo=None,
                                 componente=componente3, campus_turma=sala.campus, local=sala, ano=2020,
                                 periodo=2, descricao_horario='35T12', capacidade_aluno=25, tipo='REGULAR')

    SugestaoTurma.objects.create(codigo_turma='02', docente=docente2, matricula_docente_externo=None,
                                 componente=componente3, campus_turma=sala.campus, local=sala, ano=2020,
                                 periodo=2, descricao_horario='35T34', capacidade_aluno=25, tipo='REGULAR')
    print(Turma.objects.filter(componente=componente3))


def remover_sugestoes_turmas():
    try:
        SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999).delete()
        SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99998).delete()
        SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99997).delete()
        SugestaoTurma.objects.get(codigo_turma='02', componente__id_componente=99997).delete()
    except SugestaoTurma.DoesNotExist:
        print('SugestaoTurma não Existe!')
