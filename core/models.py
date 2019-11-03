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
        return self.nome + ' - ' + self.sigla


class Curso(models.Model):
    """
        Um curso tem: código, nome, nível de ensino, grau acadêmico, modalidade, turno e centro.
    """
    codigo = models.IntegerField(unique=True)
    nome = models.CharField(max_length=200)
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


class ComponenteCurricular(models.Model):
    """
        Um componente curricular tem código, nome, ementa, departamento, carga horária, equivalências, requisitos, data de criação.
    """
    id_componente = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10)
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

    def __str__(self):
        return self.codigo + ' - ' + self.nome


class OrganizacaoCurricular(models.Model):
    id_curriculo_componente = models.IntegerField(unique=True)
    estrutura = models.ForeignKey(EstruturaCurricular, on_delete=models.PROTECT)
    componente = models.ForeignKey(ComponenteCurricular, on_delete=models.PROTECT)
    semestre = models.IntegerField()
    tipo_vinculo = models.CharField(max_length=50)
    nivel = models.CharField(max_length=50)

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

    def __str__(self):
        return self.dia + self.turno + self.ordem
