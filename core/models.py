from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class ComponenteCurricular(models.Model):
    """
        Um componente curricular tem código, nome, ementa, departamento, carga horária, equivalências, requisitos, data de criação.
    """
    codigo = models.IntegerField()
    nome = models.CharField(max_length=200)
    ementa = models.CharField(max_length=200)
    departamento = models.CharField(max_length=200)
    carga_horaria = models.IntegerField()


class EstruturaCurricular(models.Model):
    codigo = models.IntegerField()
    sigla = models.CharField(max_length=10)
    nome = models.CharField(max_length=200)
    ano_periodo = models.CharField(max_length=10)

class OrganizacaoCurricular(models.Model):
    estrutura = models.ForeignKey(EstruturaCurricular, on_delete=models.PROTECT)
    componente = models.ForeignKey(ComponenteCurricular, on_delete=models.PROTECT)
    periodo = models.IntegerField()
    obrigatoria = models.BooleanField()

class Horario(models.Model):
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
    ordem = models.CharField(max_length=1, choices= ORDENS)
    turno = models.CharField(max_length=10, choices= TURNOS)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    class Meta:
        unique_together = ("ordem", "turno")

    def __str__(self):
        return self.ordem + self.turno
