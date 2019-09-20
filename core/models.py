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
    codigo = models.CharField(max_length=10)
    nome = models.CharField(max_length=200)
    ementa = models.TextField(max_length=500)
    ch_total = models.IntegerField()
    ch_teorica = models.IntegerField()
    ch_pratica = models.IntegerField()
    requisito = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='pre_requisitos')
    corequisito = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='co_requisitos')
    equivalencia = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='equivalencias')
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)

    def __str__(self):
        return self.codigo + ' - ' + self.nome


class EstruturaCurricular(models.Model):
    codigo = models.IntegerField(unique=True)
    sigla = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=200)
    ano_periodo = models.CharField(max_length=10)


class OrganizacaoCurricular(models.Model):
    estrutura = models.ForeignKey(EstruturaCurricular, on_delete=models.PROTECT)
    componente = models.ForeignKey(ComponenteCurricular, on_delete=models.PROTECT)
    periodo = models.IntegerField()
    obrigatoria = models.BooleanField()


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
        return  self.dia + self.turno + self.ordem
