import django_filters

from core.models import Sala, Docente


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
