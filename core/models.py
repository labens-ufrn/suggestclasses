from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class ComponenteCurricular(models.Model):
    '''
        Um componente curricular tem código, nome, ementa, departamento, carga horária, equivalências, requisitos, data de criação.
    '''
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
