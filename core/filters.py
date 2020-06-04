import django_filters

from core.models import Sala, Docente, Enquete


class SalaFilter(django_filters.FilterSet):
    CAMPUS_CHOICES = (
        ("1", "Campus Caicó"),
        ("2", "Campus Currais Novos"),
    )
    campus = django_filters.ChoiceFilter(choices=CAMPUS_CHOICES)

    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome:')
    sigla = django_filters.CharFilter(lookup_expr='icontains', label='Sigla:')

    class Meta:
        model = Sala
        fields = ['nome', 'sigla', 'centro', 'campus']


class DocenteFilter(django_filters.FilterSet):

    siape = django_filters.CharFilter(lookup_expr='icontains', label='Siape:')
    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome:')
    lotacao = django_filters.CharFilter(lookup_expr='icontains', label='Lotação:')

    class Meta:
        model = Docente
        fields = ['siape', 'nome', 'lotacao']


class EnqueteFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        ("1", "Cadastrada"),
        ("2", "Ativa"),
        ("3", "Fechada"),
    )
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)

    nome = django_filters.CharFilter(lookup_expr='icontains', label='Nome:')
    curso = django_filters.CharFilter(lookup_expr='icontains', label='Curso:')

    class Meta:
        model = Enquete
        fields = ['nome', 'curso', 'periodo', 'status']
