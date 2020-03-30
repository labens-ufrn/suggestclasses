import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from dateutil.parser import parse
from core.models import Centro, Departamento, ComponenteCurricular, Docente, EstruturaCurricular, Curso


def criar_dados():
    print("Povoando Dados para Testes ...")

    criar_centro()
    criar_cursos()
    criar_departamentos()
    criar_componentes()
    criar_estruturas()
    criar_docentes()


def remover_dados():
    print("Removendo Dados dos Testes ...")
    try:
        Docente.objects.get(siape=9999999).delete()
    except Docente.DoesNotExist:
        print('Docente não Existe!')
    try:
        EstruturaCurricular.objects.get(id_curriculo=999999999).delete()
    except EstruturaCurricular.DoesNotExist:
        print('EstruturaCurricular não Existe!')
    try:
        ComponenteCurricular.objects.get(id_componente=99999).delete()
    except ComponenteCurricular.DoesNotExist:
        print('ComponenteCurricular não Existe!')
    try:
        Departamento.objects.get(id_unidade=9998).delete()
    except Departamento.DoesNotExist:
        print('Departamento não Existe!')
    try:
        Curso.objects.get(codigo=9999).delete()
    except Curso.DoesNotExist:
        print('Curso não Existe!')
    try:
        Centro.objects.get(id_unidade=9999).delete()
    except Centro.DoesNotExist:
        print('Centro não Existe!')


def criar_centro():
    Centro.objects.create(id_unidade=9999, codigo=9999, nome='Centro de Teste',
                          sigla='CTESTE', endereco='Rua Joaquim Gregório, Penedo, Caicó - RN',
                          site='https://www.ceres.ufrn.br/')


def criar_cursos():
    centro = Centro.objects.get(id_unidade=9999)
    Curso.objects.create(codigo=9999, nome='Curso Teste', nivel='Graduação', grau='Bacharelado',
                         modalidade='Presencial', turno='Matutino e Vespertino', centro=centro)


def criar_departamentos():
    centro = Centro.objects.get(id_unidade=9999)
    Departamento.objects.create(id_unidade=9998, codigo=9998, nome='Departamento de Teste', sigla='DTS',
                                endereco='Rua Joaquim Gregório, Penedo, Caicó - RN',
                                centro=centro)


def criar_componentes():
    departamento = Departamento.objects.get(id_unidade=9998)
    ComponenteCurricular.objects.create(id_componente=99999, tipo='DISCIPLINA',
                                        codigo='DCT9999', nivel='G', nome='BANCO DE DADOS',
                                        ch_teorica=30, ch_pratica=30, ch_estagio=0,
                                        ch_total=60, ch_docente=60, ch_ead=0,
                                        cr_max_ead=0, equivalencia='( BSI2201 )',
                                        requisito='( ( BSI1106 ) OU ( DCT1106 ) )', corequisito='',
                                        ementa='ementa', modalidade='Presencial', departamento=departamento)


def criar_estruturas():
    curso = Curso.objects.get(codigo=9999)
    EstruturaCurricular.objects.create(id_curriculo=999999999, codigo='01',
                                       nome='Curso Teste - CAICÓ - MT - BACHARELADO', semestre_conclusao_minimo=8,
                                       semestre_conclusao_ideal=8, semestre_conclusao_maximo=12,
                                       meses_conclusao_minimo=None, meses_conclusao_ideal=None,
                                       meses_conclusao_maximo=None, cr_total_minimo=148, ch_total_minima=3000,
                                       ch_optativas_minima=300, ch_complementar_minima=180, max_eletivos=240,
                                       ch_nao_atividade_obrigatoria=2220, cr_nao_atividade_obrigatorio=148,
                                       ch_atividade_obrigatoria=480, cr_minimo_semestre=8, cr_ideal_semestre=24,
                                       cr_maximo_semestre=28, ch_minima_semestre=120, ch_ideal_semestre=None,
                                       ch_maxima_semestre=0, periodo_entrada_vigor=1, ano_entrada_vigor=2020,
                                       observacao='', curso=curso)


def criar_docentes():
    departamento = Departamento.objects.get(id_unidade=9998)
    Docente.objects.create(siape=9999999, nome='Nome Docente Teste', sexo='M', formacao='Mestrado',
                           tipo_jornada_trabalho='Dedicação Exclusiva', vinculo='Ativo Permanente',
                           categoria='PROFESSOR DO MAGISTERIO SUPERIOR', classe_funcional='Classe C - Adjunto',
                           id_unidade_lotacao=departamento.id_unidade,
                           lotacao='Departamento de Teste', admissao=parse('2020/03/30'))
