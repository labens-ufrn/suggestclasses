from django.db import models


class Centro(models.Model):
    """
        Um centro tem identificador, código, nome, sigla, endereço e site.
    """
    id_unidade = models.IntegerField(unique=True)
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200, unique=True)
    sigla = models.CharField(max_length=15, unique=True)
    endereco = models.CharField(max_length=250, blank=True, null=True)
    site = models.CharField(max_length=250)

    def __str__(self):
        return self.nome + ' - ' + self.sigla


class Departamento(models.Model):
    """
        Um departamento tem identificador, código, nome, sigla, endereço e site.
    """
    id_unidade = models.IntegerField(unique=True)
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200, unique=True)
    sigla = models.CharField(max_length=15, unique=True)
    endereco = models.CharField(max_length=250, blank=True, null=True)
    site = models.CharField(max_length=250)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome + ' - ' + self.sigla + '/' + self.centro.sigla


class Docente(models.Model):
    siape = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200)
    sexo = models.CharField(max_length=10)
    formacao = models.CharField(max_length=50)
    tipo_jornada_trabalho = models.CharField(max_length=50)
    vinculo = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    classe_funcional = models.CharField(max_length=50)
    id_unidade_lotacao = models.IntegerField()
    lotacao = models.CharField(max_length=150)
    admissao = models.DateField()

    def primeiro_nome(self):
        split_nome = self.nome.split(' ')
        return split_nome[0]

    def __str__(self):
        return self.siape.__str__() + ' - ' + self.nome + ' - ' + self.lotacao


class Curso(models.Model):
    """
        Um curso tem: código, nome, nível de ensino, grau acadêmico, modalidade, turno e centro.
    """
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200)
    coordenador = models.ForeignKey(Docente, on_delete=models.PROTECT, blank=True, null=True)
    nivel = models.CharField(max_length=250)
    grau = models.CharField(max_length=250)
    modalidade = models.CharField(max_length=250)
    turno = models.CharField(max_length=50)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome + ' - ' + self.grau + ' - ' + self.centro.sigla


class Sala(models.Model):
    """
        Uma sala tem um número, um nome, capacidade, tamanho, bloco.
    """
    nome = models.CharField(max_length=200, blank=True, null=True)
    sigla = models.CharField(max_length=10)
    capacidade = models.IntegerField()
    tamanho = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bloco = models.CharField(max_length=10)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT)
    campus = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nome + ' (' + self.capacidade.__str__() + ')' + ' - ' + self.bloco


class ComponenteCurricular(models.Model):
    """
        Um componente curricular tem código, nome, ementa, departamento, carga horária,
        equivalências, requisitos, data de criação.
    """
    id_componente = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=50)
    codigo = models.CharField(max_length=25)
    nivel = models.CharField(max_length=50)
    nome = models.CharField(max_length=200)
    ementa = models.TextField(max_length=500)
    ch_teorica = models.IntegerField()
    ch_pratica = models.IntegerField()
    ch_estagio = models.IntegerField()
    ch_total = models.IntegerField()
    ch_docente = models.IntegerField()
    ch_ead = models.IntegerField()
    cr_max_ead = models.IntegerField()
    equivalencia = models.TextField(max_length=500)
    requisito = models.TextField(max_length=500)
    corequisito = models.TextField(max_length=500)
    modalidade = models.CharField(max_length=200)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'componente curricular'
        verbose_name_plural = 'componentes curriculares'

    def __str__(self):
        return self.codigo + ' - ' + self.nome


class EstruturaCurricular(models.Model):
    id_curriculo = models.IntegerField(unique=True)
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=200)
    semestre_conclusao_minimo = models.IntegerField(null=True)
    semestre_conclusao_ideal = models.IntegerField(null=True)
    semestre_conclusao_maximo = models.IntegerField(null=True)
    meses_conclusao_minimo = models.IntegerField(null=True)
    meses_conclusao_ideal = models.IntegerField(null=True)
    meses_conclusao_maximo = models.IntegerField(null=True)
    cr_total_minimo = models.IntegerField(null=True)
    ch_total_minima = models.IntegerField(null=True)
    ch_optativas_minima = models.IntegerField(null=True)
    ch_complementar_minima = models.IntegerField(null=True)
    max_eletivos = models.IntegerField(null=True)
    ch_nao_atividade_obrigatoria = models.IntegerField(null=True)
    cr_nao_atividade_obrigatorio = models.IntegerField(null=True)
    ch_atividade_obrigatoria = models.IntegerField(null=True)
    cr_minimo_semestre = models.IntegerField(null=True)
    cr_ideal_semestre = models.IntegerField(null=True)
    cr_maximo_semestre = models.IntegerField(null=True)
    ch_minima_semestre = models.IntegerField(null=True)
    ch_ideal_semestre = models.IntegerField(null=True)
    ch_maxima_semestre = models.IntegerField(null=True)
    periodo_entrada_vigor = models.IntegerField(null=True)
    ano_entrada_vigor = models.IntegerField(null=True)
    observacao = models.TextField(max_length=500, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'estrutura curricular'
        verbose_name_plural = 'estruturas curriculares'

    def __str__(self):
        return self.codigo + ' - ' + self.nome


class OrganizacaoCurricular(models.Model):
    id_curriculo_componente = models.IntegerField(unique=True)
    estrutura = models.ForeignKey(EstruturaCurricular, on_delete=models.PROTECT)
    componente = models.ForeignKey(ComponenteCurricular, on_delete=models.PROTECT)
    semestre = models.IntegerField()
    tipo_vinculo = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'organização curricular'
        verbose_name_plural = 'organizações curriculares'

    def __str__(self):
        return self.componente.nome + ' - ' + self.estrutura.nome


class Horario(models.Model):
    DIAS = (
        ('1', 'Domingo'),
        ('2', 'Segunda'),
        ('3', 'Terça'),
        ('4', 'Quarta'),
        ('5', 'Quinta'),
        ('6', 'Sexta'),
        ('7', 'Sábado'),
    )

    ORDENS = (
        ('1', 'Primeiro Horário'),
        ('2', 'Segundo Horário'),
        ('3', 'Terceiro Horário'),
        ('4', 'Quarto Horário'),
        ('5', 'Quinto Horário'),
        ('6', 'Sexto Horário'),
    )

    TURNOS = (
        ('M', 'Manhã'),
        ('T', 'Tarde'),
        ('N', 'Noite'),
    )

    dia = models.CharField(max_length=1, choices=DIAS)
    turno = models.CharField(max_length=10, choices=TURNOS)
    ordem = models.CharField(max_length=1, choices=ORDENS)
    hora_inicio = models.TimeField()
    hora_final = models.TimeField()

    class Meta:
        unique_together = ("dia", "turno", "ordem")

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.dia == other.dia and self.turno == other.turno and self.ordem == other.ordem

    def __str__(self):
        return self.dia + self.turno + self.ordem


class Turma(models.Model):
    id_turma = models.IntegerField()
    codigo_turma = models.CharField(max_length=50)
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT, null=True, blank=True)
    matricula_docente_externo = models.IntegerField(null=True, blank=True)
    observacao = models.CharField(max_length=250, blank=True)
    componente = models.ForeignKey(ComponenteCurricular, on_delete=models.PROTECT)
    ch_dedicada_periodo = models.IntegerField()
    nivel_ensino = models.CharField(max_length=50)
    campus_turma = models.CharField(max_length=50)
    local = models.CharField(max_length=50)
    ano = models.IntegerField()
    periodo = models.IntegerField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    descricao_horario = models.CharField(max_length=150)
    total_solicitacoes = models.IntegerField(null=True)
    capacidade_aluno = models.IntegerField()
    tipo = models.CharField(max_length=50)
    distancia = models.BooleanField()
    data_consolidacao = models.DateField(null=True)
    agrupadora = models.BooleanField(blank=True)
    id_turma_agrupadora = models.IntegerField(null=True, blank=True)
    qtd_aulas_lancadas = models.IntegerField(null=True)
    situacao_turma = models.CharField(max_length=50)
    convenio = models.CharField(max_length=50, null=True, blank=True)
    modalidade_participantes = models.CharField(max_length=50)

    class Meta:
        unique_together = ('codigo_turma', 'componente', 'ano', 'periodo')

    def __str__(self):
        return self.id_turma.__str__() + ' - ' + self.codigo_turma + ' - ' + self.componente.__str__() + ' - ' \
               + self.docente.__str__() + ' - ' + self.descricao_horario


class SugestaoTurma(models.Model):
    codigo_turma = models.CharField(max_length=50)
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT, null=True, blank=True)
    matricula_docente_externo = models.IntegerField(null=True, blank=True)
    componente = models.ForeignKey(ComponenteCurricular, on_delete=models.PROTECT)
    campus_turma = models.CharField(max_length=50)
    local = models.ForeignKey(Sala, on_delete=models.PROTECT, null=True, blank=True)
    ano = models.IntegerField()
    periodo = models.IntegerField()
    descricao_horario = models.CharField(max_length=150)
    capacidade_aluno = models.IntegerField()
    tipo = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('codigo_turma', 'componente', 'ano', 'periodo')
        verbose_name = 'sugestão de turma'
        verbose_name_plural = 'sugestões de turmas'

    def __str__(self):
        return self.codigo_turma + ' - ' + self.componente.__str__() + ' - ' \
               + self.docente.primeiro_nome() + ' (' + self.docente.siape.__str__() + ') - ' \
               + self.descricao_horario


class FuncaoGratificada(models.Model):
    """
    Modelo para as funções gratificadas (designações).
    """
    siape = models.IntegerField()
    nome = models.CharField(max_length=200)
    situacao_servidor = models.CharField(max_length=25)
    id_unidade = models.IntegerField()
    lotacao = models.CharField(max_length=200)
    sigla = models.CharField(max_length=15)
    inicio = models.DateField()
    fim = models.DateField(null=True)
    id_unidade_designacao = models.IntegerField()
    unidade_designacao = models.CharField(max_length=200)
    atividade = models.CharField(max_length=100)
    observacoes = models.CharField(max_length=200, null=True)


class Discente(models.Model):
    """
    Modelo para os dados dos Discentes.
    """
    matricula = models.IntegerField()
    nome_discente = models.CharField(max_length=200, null=False)
    sexo = models.CharField(max_length=1)
    ano_ingresso = models.IntegerField()
    periodo_ingresso = models.IntegerField()
    forma_ingresso = models.CharField(max_length=100)
    tipo_discente = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    sigla_nivel_ensino = models.CharField(max_length=5)
    nivel_ensino = models.CharField(max_length=50)
    id_curso = models.CharField(max_length=100)
    nome_curso = models.CharField(max_length=200, null=False)
    modalidade_educacao = models.CharField(max_length=50)
    id_unidade = models.IntegerField()
    nome_unidade = models.CharField(max_length=200)
    id_unidade_gestora = models.IntegerField()
    nome_unidade_gestora = models.CharField(max_length=200)

    def __str__(self):
        return self.nome + ' (' + self.matricula.__str__() + ') - ' \
               + self.nome_curso + ' (' + self.nome_unidade + ' - ' \
               + self.nome_unidade_gestora + ') - '
