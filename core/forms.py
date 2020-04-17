from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import Form, ModelForm

from core.bo.sevices import get_cc_by_estrutura
from core.bo.sistemas import get_estrutura_sistemas_dct
from core.models import SugestaoTurma, Docente, ComponenteCurricular, EstruturaCurricular


class CadastroUsuarioForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True,
                               help_text='Obrigatório. 30 caracteres ou menos. '
                                         'Letras minúsculas, números e @ . + - _ apenas.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label='Primeiro Nome')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.', label='Sobrenome')
    matricula = forms.CharField(max_length=15, required=True, help_text='Obrigatório. Sua matrícula na UFRN.',
                                label='Matrícula')
    email = forms.EmailField(max_length=254, required=True, help_text='Obrigatório. Informe um e-mail válido.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'matricula', 'email', 'password1', 'password2',)


class SugestaoTurmaForm(ModelForm):
    docente = forms.ModelChoiceField(queryset=Docente.objects.all().order_by('nome', 'siape'), label='Docente',
                                     required=False)

    componente = forms.ModelChoiceField(queryset=ComponenteCurricular.objects.all().order_by('nome', 'codigo'),
                                        label='Componente Curricular')

    descricao_horario = forms.CharField(label='Descrição do Horário',
                                        widget=forms.TextInput(attrs={'placeholder': 'Ex: 24M34'}))

    capacidade_aluno = forms.CharField(label='Vagas', max_length=3,
                                       help_text='Obrigatório. As vagas deve ser menor que a capacidade da sala.')

    def __init__(self, *args, **kwargs):
        estrutura = kwargs.pop('estrutura')
        super(SugestaoTurmaForm, self).__init__(*args, **kwargs)
        self.fields['componente'].queryset = get_cc_by_estrutura(estrutura)

    class Meta:
        model = SugestaoTurma
        fields = ['codigo_turma', 'componente', 'docente', 'descricao_horario',
                  'local', 'capacidade_aluno']
        widgets = {
            'codigo_turma': forms.TextInput(attrs={'placeholder': '01'}),
        }
