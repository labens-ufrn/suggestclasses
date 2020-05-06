import django
django.setup()
import threading

from dateutil.parser import parse
from django.contrib.auth.models import User, Group

from core.models import Centro, Departamento, ComponenteCurricular, Docente, EstruturaCurricular, Curso, \
    OrganizacaoCurricular, Turma, Sala, SugestaoTurma, Discente, FuncaoGratificada, Horario
from dados.povoar_horarios import povoar_horarios


class PovoarDadosTestes(object):

    class __OnlyOne:
        def __init__(self):
            # Buscar esses dados em algum arquivo Config.
            self.povoar = True
            self.remover = True

        def __str__(self):
            return self.__hash__().__str__() + ' povoar: ' + self.povoar.__str__() + ' remover: ' + self.remover.__str__()

    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def load(cls):  # __new__ always a classmethod
        # check for the singleton instance
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls.__OnlyOne()

        # return the singleton instance
        return cls.__singleton_instance

    def __getattr__(self, name):
        return getattr(self.__singleton_instance, name)

    def __setattr__(self, name):
        return setattr(self.__singleton_instance, name)


def criar_dados():
    dados = PovoarDadosTestes.load()
    print('Criar Dados: ' + dados.__str__())
    if dados.povoar:
        print('...... povoando dados ......')
        criar_tudo()
        dados.povoar = True


def remover_dados():
    dados = PovoarDadosTestes.load()
    if dados.remover:
        print()
        print('...... removendo dados ......')
        remover_tudo()
        dados.povoar = True


def criar_tudo():
    criar_horarios()
    criar_usuario()
    criar_grupos()
    criar_centro()
    criar_salas()
    criar_departamentos()
    criar_docentes()
    criar_funcao_gratificada()
    criar_cursos()
    criar_componentes()
    criar_estruturas()
    criar_curriculos()
    criar_turmas()
    criar_sugestoes_turmas()
    criar_discentes()


def remover_tudo():
    remover_discentes()
    remover_sugestoes_turmas()
    remover_turmas()
    remover_curriculos()
    remover_estruturas()
    remover_componentes()
    remover_cursos()
    remover_funcao_gratificada()
    remover_docentes()
    remover_departamentos()
    remover_salas()
    remover_centro()
    remover_grupos()
    remover_usuario()


def criar_horarios():
    povoar_horarios()


def criar_usuario():
    if not User.objects.filter(username='john'):
        User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    if not User.objects.filter(username='docente1'):
        User.objects.create_user('docente1', 'docente1@thebeatles.com', 'johnpassword')
    if not User.objects.filter(username='docente2'):
        User.objects.create_user('docente2', 'docente2@thebeatles.com', 'johnpassword')
    if not User.objects.filter(username='docente3'):
        User.objects.create_user('docente3', 'docente3@thebeatles.com', 'johnpassword')


def criar_grupos():
    new_group, created = Group.objects.get_or_create(name='ChefesTeste')

    # Code to add permission to group ???
    # ct = ContentType.objects.get_for_model(SugestaoTurma)

    # Now what - Say I want to add 'Can add project' permission to new_group?
    # permission = Permission.objects.create(codename='core.mudar_sugestaoturma',
    #                                        name='Can change sugestão de turma',
    #                                        content_type=ct)
    # new_group.permissions.add(permission)

    new_group, created = Group.objects.get_or_create(name='DocentesTeste')
    # Code to add permission to group ???
    # ct = ContentType.objects.get_for_model(SugestaoTurma)

    # Now what - Say I want to add 'Can add project' permission to new_group?
    # permission = Permission.objects.create(codename='core.ver_sugestaoturma',
    #                                        name='Can view sugestão de turma',
    #                                        content_type=ct)
    # new_group.permissions.add(permission)


def remover_grupos():
    try:
        Group.objects.get(name='DocentesTeste').delete()
        Group.objects.get(name='ChefesTeste').delete()
    except Group.DoesNotExist:
        print('.', end="")


def criar_discentes():
    if not Discente.objects.filter(matricula='20209876543').exists():
        Discente.objects.create(matricula='20209876543', nome_discente='Zé Silva', sexo='M',
                                ano_ingresso=2020, periodo_ingresso=1,
                                forma_ingresso='SiSU', tipo_discente='REGULAR', status='ATIVO',
                                sigla_nivel_ensino='G', nivel_ensino='GRADUAÇÃO',
                                id_curso='7191770', nome_curso='SISTEMAS DE INFORMAÇÃO',
                                modalidade_educacao='PRESENCIAL',
                                id_unidade=1482, nome_unidade='CENTRO DE  ENSINO SUPERIOR DO SERIDÓ',
                                id_unidade_gestora=1482, nome_unidade_gestora='CENTRO DE  ENSINO SUPERIOR DO SERIDÓ')


def criar_centro():
    if not Centro.objects.filter(id_unidade=9999).exists():
        Centro.objects.create(id_unidade=9999, codigo=9999, nome='Centro de Teste',
                              sigla='CTESTE', endereco='Rua Joaquim Gregório, Penedo, Caicó - RN',
                              site='https://www.ceres.ufrn.br/')


def remover_centro():
    try:
        Centro.objects.get(id_unidade=9999).delete()
    except Centro.DoesNotExist:
        print('.', end="")


def remover_usuario():
    try:
        User.objects.get(username='john').delete()
        User.objects.get(username='docente1').delete()
        User.objects.get(username='docente2').delete()
        User.objects.get(username='docente3').delete()
    except User.DoesNotExist:
        print('.', end="")


def remover_discentes():
    try:
        Discente.objects.get(matricula=20209876543).delete()
    except Discente.DoesNotExist:
        print('.', end="")


def criar_salas():
    centro = Centro.objects.get(id_unidade=9999)
    if not Sala.objects.filter(nome='Sala A01', sigla='A01', capacidade=25, tamanho=None, bloco='Bloco A',
                               centro=centro, campus='Campus Teste').exists():
        Sala.objects.create(nome='Sala A01', sigla='A01', capacidade=25, tamanho=None, bloco='Bloco A',
                            centro=centro, campus='Campus Teste')


def remover_salas():
    try:
        Sala.objects.get(sigla='A01', bloco='Bloco A', centro__id_unidade=9999, campus='Campus Teste').delete()
    except Sala.DoesNotExist:
        print('.', end="")


def criar_departamentos():
    centro = Centro.objects.get(id_unidade=9999)
    if not Departamento.objects.filter(id_unidade=9998).exists():
        Departamento.objects.create(id_unidade=9998, codigo=9998, nome='Departamento de Teste', sigla='DTS',
                                    endereco='Rua Joaquim Gregório, Penedo, Caicó - RN',
                                    centro=centro)


def remover_departamentos():
    try:
        Departamento.objects.get(id_unidade=9998).delete()
    except Departamento.DoesNotExist:
        print('.', end="")


def criar_docentes():
    departamento = Departamento.objects.get(id_unidade=9998)
    grupo_docentes = Group.objects.get(name='DocentesTeste')
    grupo_chefes = Group.objects.get(name='ChefesTeste')

    usuario1 = User.objects.get(username='docente1')
    usuario1.groups.add(grupo_docentes)
    usuario1.save()

    usuario2 = User.objects.get(username='docente2')
    usuario2.groups.add(grupo_docentes)
    usuario2.groups.add(grupo_chefes)
    usuario2.save()

    usuario3 = User.objects.get(username='docente3')
    usuario3.groups.add(grupo_docentes)
    usuario3.save()

    if not Docente.objects.filter(siape=9999999).exists():
        Docente.objects.create(siape=9999999, nome='Nome Docente Teste 1', sexo='M', formacao='Mestrado',
                               tipo_jornada_trabalho='Dedicação Exclusiva', vinculo='Ativo Permanente',
                               categoria='PROFESSOR DO MAGISTERIO SUPERIOR', classe_funcional='Classe C - Adjunto',
                               id_unidade_lotacao=departamento.id_unidade,
                               lotacao='Departamento de Teste', admissao=parse('2020/03/30'),
                               usuario=usuario1)
    if not Docente.objects.filter(siape=9999998).exists():
        Docente.objects.create(siape=9999998, nome='Nome Docente Chefe', sexo='F', formacao='Doutorado',
                               tipo_jornada_trabalho='Dedicação Exclusiva', vinculo='Ativo Permanente',
                               categoria='PROFESSOR DO MAGISTERIO SUPERIOR', classe_funcional='Classe D - Adjunto',
                               id_unidade_lotacao=departamento.id_unidade,
                               lotacao='Departamento de Teste', admissao=parse('2020/04/17'),
                               usuario=usuario2)
    if not Docente.objects.filter(siape=9999997).exists():
        Docente.objects.create(siape=9999997, nome='Nome Docente Teste 2', sexo='F', formacao='Doutorado',
                               tipo_jornada_trabalho='Dedicação Exclusiva', vinculo='Ativo Permanente',
                               categoria='PROFESSOR DO MAGISTERIO SUPERIOR', classe_funcional='Classe D - Adjunto',
                               id_unidade_lotacao=departamento.id_unidade,
                               lotacao='Departamento de Teste', admissao=parse('2020/03/30'),
                               usuario=usuario3)
    if not Docente.objects.filter(siape=9999996).exists():
        Docente.objects.create(siape=9999996, nome='Nome Docente Teste 4', sexo='F', formacao='Doutorado',
                               tipo_jornada_trabalho='Dedicação Exclusiva', vinculo='Ativo Permanente',
                               categoria='PROFESSOR DO MAGISTERIO SUPERIOR', classe_funcional='Classe D - Adjunto',
                               id_unidade_lotacao=departamento.id_unidade,
                               lotacao='Departamento de Teste', admissao=parse('2020/03/30'))


def remover_docentes():
    try:
        Docente.objects.get(siape=9999999).delete()
        Docente.objects.get(siape=9999998).delete()
        Docente.objects.get(siape=9999997).delete()
        Docente.objects.get(siape=9999996).delete()
    except Docente.DoesNotExist:
        print('.', end="")


def criar_funcao_gratificada():
    departamento = Departamento.objects.get(id_unidade=9998)
    docente1 = Docente.objects.get(siape=9999998)
    inicio = parse('2019/11/19')
    fim = parse('2021/11/18')
    atividade = 'CHEFE DE DEPARTAMENTO'

    if not FuncaoGratificada.objects.filter(
            siape=9999998, id_unidade=docente1.id_unidade_lotacao, inicio=inicio, atividade=atividade).exists():
        FuncaoGratificada.objects.create(siape=9999998, nome=docente1.nome, situacao_servidor=docente1.vinculo,
                                         id_unidade=docente1.id_unidade_lotacao, lotacao=departamento.nome,
                                         sigla=departamento.sigla, inicio=inicio, fim=fim,
                                         id_unidade_designacao=departamento.id_unidade,
                                         unidade_designacao=departamento.nome, atividade='CHEFE DE DEPARTAMENTO',
                                         observacoes='')


def remover_funcao_gratificada():
    id_unidade = 9998
    siape = 9999998
    inicio = parse('2019/11/19')
    atividade = 'CHEFE DE DEPARTAMENTO'

    try:
        FuncaoGratificada.objects.get(
            siape=siape, id_unidade=id_unidade, inicio=inicio, atividade=atividade).delete()
    except FuncaoGratificada.DoesNotExist:
        print('.', end="")


def criar_cursos():
    centro = Centro.objects.get(id_unidade=9999)
    docente1 = Docente.objects.get(siape=9999999)
    docente2 = Docente.objects.get(siape=9999997)

    if not Curso.objects.filter(codigo=9999).exists():
        Curso.objects.create(codigo=9999, nome='Curso Teste 1', coordenador=docente1, nivel='Graduação',
                             grau='Bacharelado', modalidade='Presencial', turno='Matutino e Vespertino',
                             centro=centro)
    if not Curso.objects.filter(codigo=9998).exists():
        Curso.objects.create(codigo=9998, nome='Curso Teste 2', coordenador=docente2, nivel='Graduação',
                             grau='Licenciatura', modalidade='Presencial', turno='Matutino e Vespertino',
                             centro=centro)


def remover_cursos():
    try:
        Curso.objects.get(codigo=9999).delete()
        Curso.objects.get(codigo=9998).delete()
    except Curso.DoesNotExist:
        print('.', end="")


def criar_componentes():
    departamento = Departamento.objects.get(id_unidade=9998)
    if not ComponenteCurricular.objects.filter(id_componente=99999).exists():
        ComponenteCurricular.objects.create(id_componente=99999, tipo='DISCIPLINA',
                                            codigo='DCT9999', nivel='G', nome='BANCO DE DADOS',
                                            ch_teorica=30, ch_pratica=30, ch_estagio=0,
                                            ch_total=60, ch_docente=60, ch_ead=0,
                                            cr_max_ead=0, equivalencia='( BSI2201 )',
                                            requisito='( ( BSI1106 ) OU ( DCT1106 ) )', corequisito='',
                                            ementa='ementa', modalidade='Presencial', departamento=departamento)
    if not ComponenteCurricular.objects.filter(id_componente=99998).exists():
        ComponenteCurricular.objects.create(id_componente=99998, tipo='DISCIPLINA',
                                            codigo='DCT9998', nivel='G', nome='ENGENHARIA DE SOFTWARE',
                                            ch_teorica=30, ch_pratica=30, ch_estagio=0,
                                            ch_total=60, ch_docente=60, ch_ead=0,
                                            cr_max_ead=0, equivalencia='( BSI2301 )',
                                            requisito='( ( BSI1106 ) OU ( DCT1106 ) )', corequisito='',
                                            ementa='ementa', modalidade='Presencial', departamento=departamento)
    if not ComponenteCurricular.objects.filter(id_componente=99997).exists():
        ComponenteCurricular.objects.create(id_componente=99997, tipo='DISCIPLINA',
                                            codigo='DCT9997', nivel='G', nome='TESTE DE SOFTWARE',
                                            ch_teorica=30, ch_pratica=30, ch_estagio=0,
                                            ch_total=60, ch_docente=60, ch_ead=0,
                                            cr_max_ead=0, equivalencia='( BSI2201 )',
                                            requisito='( ( BSI1106 ) OU ( DCT1106 ) )', corequisito='',
                                            ementa='ementa', modalidade='Presencial', departamento=departamento)
    if not ComponenteCurricular.objects.filter(id_componente=99996).exists():
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
        print('.', end="")


def criar_estruturas():
    curso1 = Curso.objects.get(codigo=9999)
    curso2 = Curso.objects.get(codigo=9998)
    if not EstruturaCurricular.objects.filter(id_curriculo=999999999).exists():
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
    if not EstruturaCurricular.objects.filter(id_curriculo=999999998).exists():
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
        print('.', end="")


def criar_curriculos():
    estrutura1 = EstruturaCurricular.objects.get(id_curriculo=999999999)
    estrutura2 = EstruturaCurricular.objects.get(id_curriculo=999999998)
    componente1 = ComponenteCurricular.objects.get(id_componente=99999)
    componente2 = ComponenteCurricular.objects.get(id_componente=99998)
    componente3 = ComponenteCurricular.objects.get(id_componente=99997)
    componente4 = ComponenteCurricular.objects.get(id_componente=99996)
    if not OrganizacaoCurricular.objects.filter(id_curriculo_componente=999999).exists():
        OrganizacaoCurricular.objects.create(id_curriculo_componente=999999, estrutura=estrutura1,
                                             componente=componente1, semestre=1, tipo_vinculo='OBRIGATÓRIO',
                                             nivel='GRADUAÇÃO')
    if not OrganizacaoCurricular.objects.filter(id_curriculo_componente=999998).exists():
        OrganizacaoCurricular.objects.create(id_curriculo_componente=999998, estrutura=estrutura1,
                                             componente=componente2, semestre=1, tipo_vinculo='OBRIGATÓRIO',
                                             nivel='GRADUAÇÃO')
    if not OrganizacaoCurricular.objects.filter(id_curriculo_componente=999997).exists():
        OrganizacaoCurricular.objects.create(id_curriculo_componente=999997, estrutura=estrutura1,
                                             componente=componente3, semestre=2, tipo_vinculo='OBRIGATÓRIO',
                                             nivel='GRADUAÇÃO')
    if not OrganizacaoCurricular.objects.filter(id_curriculo_componente=999996).exists():
        OrganizacaoCurricular.objects.create(id_curriculo_componente=999996, estrutura=estrutura2,
                                             componente=componente2, semestre=1, tipo_vinculo='OBRIGATÓRIO',
                                             nivel='GRADUAÇÃO')
    if not OrganizacaoCurricular.objects.filter(id_curriculo_componente=999995).exists():
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
        print('.', end="")


def criar_turmas():
    docente1 = Docente.objects.get(siape=9999999)
    docente2 = Docente.objects.get(siape=9999997)
    componente1 = ComponenteCurricular.objects.get(id_componente=99999)
    componente2 = ComponenteCurricular.objects.get(id_componente=99998)
    componente3 = ComponenteCurricular.objects.get(id_componente=99997)
    sala = Sala.objects.get(sigla='A01', bloco='Bloco A', centro__id_unidade=9999, campus='Campus Teste')

    if not Turma.objects.filter(id_turma=99999999).exists():
        Turma.objects.create(id_turma=99999999, codigo_turma='01', docente=docente1, matricula_docente_externo=None,
                             observacao='', componente=componente1, ch_dedicada_periodo=60,
                             nivel_ensino='GRADUAÇÃO', campus_turma=sala.campus, local=sala, ano=2020,
                             periodo=1, data_inicio=parse('2020/03/30'), data_fim=parse('2020/07/30'),
                             descricao_horario='24T12', total_solicitacoes=15, capacidade_aluno=25, tipo='REGULAR',
                             distancia=False, data_consolidacao=None, agrupadora=False, id_turma_agrupadora=None,
                             qtd_aulas_lancadas=5, situacao_turma='ABERTA', convenio=None,
                             modalidade_participantes='Presencial')

    if not Turma.objects.filter(id_turma=99999998).exists():
        Turma.objects.create(id_turma=99999998, codigo_turma='01', docente=docente2, matricula_docente_externo=None,
                             observacao='', componente=componente2, ch_dedicada_periodo=60,
                             nivel_ensino='GRADUAÇÃO', campus_turma=sala.campus, local=sala, ano=2020,
                             periodo=1, data_inicio=parse('2020/03/30'), data_fim=parse('2020/07/30'),
                             descricao_horario='24T34', total_solicitacoes=20, capacidade_aluno=25, tipo='REGULAR',
                             distancia=False, data_consolidacao=None, agrupadora=False, id_turma_agrupadora=None,
                             qtd_aulas_lancadas=5, situacao_turma='ABERTA', convenio=None,
                             modalidade_participantes='Presencial')

    if not Turma.objects.filter(id_turma=99999997).exists():
        Turma.objects.create(id_turma=99999997, codigo_turma='01', docente=docente1, matricula_docente_externo=None,
                             observacao='', componente=componente3, ch_dedicada_periodo=60,
                             nivel_ensino='GRADUAÇÃO', campus_turma=sala.campus, local=sala, ano=2020,
                             periodo=1, data_inicio=parse('2020/03/30'), data_fim=parse('2020/07/30'),
                             descricao_horario='35T12', total_solicitacoes=15, capacidade_aluno=25, tipo='REGULAR',
                             distancia=False, data_consolidacao=None, agrupadora=False, id_turma_agrupadora=None,
                             qtd_aulas_lancadas=5, situacao_turma='ABERTA', convenio=None,
                             modalidade_participantes='Presencial')

    if not Turma.objects.filter(id_turma=99999996).exists():
        Turma.objects.create(id_turma=99999996, codigo_turma='02', docente=docente2, matricula_docente_externo=None,
                             observacao='', componente=componente3, ch_dedicada_periodo=60,
                             nivel_ensino='GRADUAÇÃO', campus_turma=sala.campus, local=sala, ano=2020,
                             periodo=1, data_inicio=parse('2020/03/30'), data_fim=parse('2020/07/30'),
                             descricao_horario='35T34', total_solicitacoes=15, capacidade_aluno=25, tipo='REGULAR',
                             distancia=False, data_consolidacao=None, agrupadora=False, id_turma_agrupadora=None,
                             qtd_aulas_lancadas=5, situacao_turma='ABERTA', convenio=None,
                             modalidade_participantes='Presencial')


def remover_turmas():
    try:
        Turma.objects.get(id_turma=99999999).delete()
        Turma.objects.get(id_turma=99999998).delete()
        Turma.objects.get(id_turma=99999997).delete()
        Turma.objects.get(id_turma=99999996).delete()
    except Turma.DoesNotExist:
        print('.', end="")


def criar_sugestoes_turmas():
    docente1 = Docente.objects.get(siape=9999999)
    docente2 = Docente.objects.get(siape=9999997)
    criador_chefe = Docente.objects.get(siape=9999998)
    curso = Curso.objects.get(codigo=9999)
    componente1 = ComponenteCurricular.objects.get(id_componente=99999)
    componente2 = ComponenteCurricular.objects.get(id_componente=99998)
    componente3 = ComponenteCurricular.objects.get(id_componente=99997)
    sala = Sala.objects.get(sigla='A01', bloco='Bloco A', centro__id_unidade=9999, campus='Campus Teste')

    if not SugestaoTurma.objects.filter(codigo_turma='01', componente=componente1, ano=2020, periodo=2).exists():
        SugestaoTurma.objects.create(codigo_turma='01', docente=docente1, matricula_docente_externo=None,
                                     componente=componente1, campus_turma=sala.campus, local=sala, ano=2020,
                                     periodo=2, descricao_horario='24T12', capacidade_aluno=25, tipo='REGULAR',
                                     total_solicitacoes=0, criador=criador_chefe.usuario,
                                     tipo_vinculo='OBRIGATÓRIO',
                                     semestre=1, curso=curso)

    if not SugestaoTurma.objects.filter(codigo_turma='01', componente=componente2, ano=2020, periodo=2).exists():
        SugestaoTurma.objects.create(codigo_turma='01', docente=docente2, matricula_docente_externo=None,
                                     componente=componente2, campus_turma=sala.campus, local=sala, ano=2020,
                                     periodo=2, descricao_horario='24T34', capacidade_aluno=25, tipo='REGULAR',
                                     total_solicitacoes=0, criador=criador_chefe.usuario,
                                     tipo_vinculo='OBRIGATÓRIO',
                                     semestre=1, curso=curso)

    if not SugestaoTurma.objects.filter(codigo_turma='01', componente=componente3, ano=2020, periodo=2).exists():
        SugestaoTurma.objects.create(codigo_turma='01', docente=docente1, matricula_docente_externo=None,
                                     componente=componente3, campus_turma=sala.campus, local=sala, ano=2020,
                                     periodo=2, descricao_horario='35T12', capacidade_aluno=25, tipo='REGULAR',
                                     total_solicitacoes=0, criador=criador_chefe.usuario,
                                     tipo_vinculo='OPTATIVO',
                                     semestre=2, curso=curso)

    if not SugestaoTurma.objects.filter(codigo_turma='02', componente=componente3, ano=2020, periodo=2).exists():
        SugestaoTurma.objects.create(codigo_turma='02', docente=docente2, matricula_docente_externo=None,
                                     componente=componente3, campus_turma=sala.campus, local=sala, ano=2020,
                                     periodo=2, descricao_horario='35T34', capacidade_aluno=25, tipo='REGULAR',
                                     total_solicitacoes=0, criador=criador_chefe.usuario,
                                     tipo_vinculo='OPTATIVO',
                                     semestre=2, curso=curso)


def remover_sugestoes_turmas():
    try:
        SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99999).delete()
        SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99998).delete()
        SugestaoTurma.objects.get(codigo_turma='01', componente__id_componente=99997).delete()
        SugestaoTurma.objects.get(codigo_turma='02', componente__id_componente=99997).delete()
    except SugestaoTurma.DoesNotExist:
        print('.', end="")
