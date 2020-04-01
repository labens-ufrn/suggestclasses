from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import Form, ModelForm

from core.bo.sevices import get_cc_by_estrutura
from core.bo.sistemas import get_estrutura_sistemas_dct
from core.models import SugestaoTurma, Docente, ComponenteCurricular


class CadastroAlunoForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True,
                               help_text='Obrigatório. 30 caracteres ou menos. '
                                         'Letras minúsculas, números e @ . + - _ apenas.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label='Primeiro Nome')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label='Sobrenome')
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), label='Grupo',
                                   help_text='Obrigatório. Grupo do usuário.')
    email = forms.EmailField(max_length=254, help_text='Obrigatório. Informe um e-mail válido.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'grupo', 'email', 'password1', 'password2',)


class SugestaoTurmaForm(ModelForm):
    docente = forms.ModelChoiceField(queryset=Docente.objects.all(), label='Docente')

    componente = forms.ModelChoiceField(queryset=get_cc_by_estrutura(get_estrutura_sistemas_dct()),
                                        label='Componente Curricular')

    descricao_horario = forms.CharField(label='Descrição do Horário',
                                        widget=forms.TextInput(attrs={'placeholder': 'Ex: 24M34'}))
    ANO_ATUAL = 2020
    PERIODO_ATUAL = 1
    ano = forms.CharField(initial=ANO_ATUAL)
    periodo = forms.CharField(initial=PERIODO_ATUAL)

    class Meta:
        model = SugestaoTurma
        fields = ['codigo_turma', 'componente', 'docente', 'descricao_horario',
                  'local', 'capacidade_aluno', 'ano', 'periodo']
        widgets = {
            'codigo_turma': forms.TextInput(attrs={'placeholder': '01'}),
        }
