from django.conf import settings
from django.contrib.auth.models import User
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
    site = models.CharField(max_length=250, blank=True, null=True)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT)

    def __str__(self):
        return self.nome + ' - ' + self.sigla + '/' + self.centro.sigla


class Docente(models.Model):
    siape = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200)
    sexo = models.CharField(max_length=1, blank=True, null=True)
    formacao = models.CharField(max_length=50)
    tipo_jornada_trabalho = models.CharField(max_length=50)
    vinculo = models.CharField(max_length=50)
    categoria = models.CharField(max_length=50)
    classe_funcional = models.CharField(max_length=50)
    id_unidade_lotacao = models.IntegerField()
    lotacao = models.CharField(max_length=150)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, null=True)
    admissao = models.DateField(blank=True, null=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def primeiro_nome(self):
        split_nome = self.nome.split(' ')
        return split_nome[0]

    def siglas_str(self):
        siglas = ''
        if self.departamento:
            siglas = ' - ' + self.departamento.sigla
            if self.departamento.centro:
                siglas = siglas + '/' + self.departamento.centro.sigla
        return siglas

    def __str__(self):
        return self.nome + ' (' + str(self.siape) + ')' + self.siglas_str()


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
    CAMPUS_CHOICES = (
        ("1", "Campus Caicó"),
        ("2", "Campus Currais Novos"),
    )

    nome = models.CharField(max_length=200, blank=True, null=True)
    sigla = models.CharField(max_length=25)
    capacidade = models.IntegerField()
    tamanho = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    bloco = models.CharField(max_length=25)
    centro = models.ForeignKey(Centro, on_delete=models.PROTECT)
    campus = models.CharField(max_length=1, blank=True, null=True, choices=CAMPUS_CHOICES)

    class Meta:
        unique_together = ("sigla", "bloco", "centro", "campus")

    def __str__(self):
        return self.nome + ' (' + self.capacidade.__str__() + ')' + ' - ' + \
               self.bloco + ' - ' + self.get_campus_display()


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

    def __hash__(self):
        return id(self)

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
    horarios = models.ManyToManyField(Horario, related_name='turmas')
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

    def get_curriculos(self, estrutura=None):
        if estrutura:
            return OrganizacaoCurricular.objects.get(
                componente=self.componente,
                estrutura=estrutura)
        return OrganizacaoCurricular.objects.filter(componente=self.componente)


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
    horarios = models.ManyToManyField(Horario, related_name='sugestoes')
    total_solicitacoes = models.IntegerField(null=True)
    capacidade_aluno = models.IntegerField()
    tipo = models.CharField(max_length=50, null=True, blank=True)
    semestre = models.IntegerField(null=True, blank=True)
    tipo_vinculo = models.CharField(max_length=50, null=True, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, null=True, blank=True)
    criador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('codigo_turma', 'componente', 'ano', 'periodo')
        verbose_name = 'sugestão de turma'
        verbose_name_plural = 'sugestões de turmas'

    def __str__(self):
        return self.codigo_turma + ' - ' + self.componente.__str__() + ' - ' \
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
    observacoes = models.CharField(max_length=500, null=True)

    class Meta:
        unique_together = ('siape', 'id_unidade', 'inicio', 'atividade')

    def __str__(self):
        return self.nome + ' (' + self.siape.__str__() + ') - ' \
               + self.atividade + ' (' + self.unidade_designacao + ')'


class Discente(models.Model):
    """
    Modelo para os dados dos Discentes.
    """
    matricula = models.CharField(max_length=15, unique=True)
    nome_discente = models.CharField(max_length=200, null=False)
    sexo = models.CharField(max_length=1, blank=True)
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
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.nome_discente + ' (' + self.matricula.__str__() + ') - ' \
               + self.nome_curso + ' (' + self.nome_unidade + ')'


class SolicitacaoTurma(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    solicitador = models.ForeignKey(Discente, on_delete=models.PROTECT)
    turma = models.ForeignKey(SugestaoTurma, on_delete=models.PROTECT)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('solicitador', 'turma')


class VinculoDocente(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.PROTECT)
    turma = models.ForeignKey(Turma, on_delete=models.PROTECT)
    carga_horaria = models.IntegerField()
    horarios = models.ManyToManyField(Horario, related_name='vinculos')
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('docente', 'turma')


class PeriodoLetivo(models.Model):
    STATUS_CHOICES = (
        ("1", "Consolidado"),
        ("2", "Ativo"),
        ("3", "Planejado"),
        ("4", "Suspenso"),
        ("5", "Cancelado"),
    )
    nome = models.CharField(max_length=50, null=False)
    ano = models.IntegerField()
    periodo = models.IntegerField()
    data_inicio = models.DateField()
    data_fim = models.DateField()
    data_consolidacao = models.DateField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    observacoes = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.nome + ' ' + str(self.ano) + '.' + str(self.periodo)


class Enquete(models.Model):
    """
    Uma enquete é uma consulta onde discente podem votar nos componentes curriculares de interesse.
    """
    STATUS_CHOICES = (
        ("1", "Cadastrada"),
        ("2", "Ativa"),
        ("3", "Fechada"),
    )
    nome = models.CharField(max_length=200, null=False)
    descricao = models.CharField(max_length=500, null=True)
    numero_votos = models.IntegerField()
    data_hora_inicio = models.DateTimeField()
    data_hora_fim = models.DateTimeField(blank=True, null=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    periodo = models.ForeignKey(PeriodoLetivo, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('nome', 'curso')

    def __str__(self):
        return self.nome + ' (' + self.curso.nome + ')'


class VotoTurma(models.Model):
    enquete = models.ForeignKey(Enquete, on_delete=models.PROTECT, related_name='votos')
    discente = models.ForeignKey(Discente, on_delete=models.PROTECT)
    componente = models.ForeignKey(ComponenteCurricular, on_delete=models.PROTECT)
    horarios = models.ManyToManyField(Horario)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('enquete', 'discente', 'componente')

    def __str__(self):
        return str(self.componente) + ' (' + self.discente.nome_discente + ')'
