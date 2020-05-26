from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import Form, ModelForm

from core.bo.sevices import get_cc_by_estrutura
from core.bo.sistemas import get_estrutura_sistemas_dct
from core.models import SugestaoTurma, Docente, ComponenteCurricular, EstruturaCurricular, Departamento


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
    componente = forms.ModelChoiceField(queryset=ComponenteCurricular.objects.all().order_by('nome', 'codigo'),
                                        label='Componente Curricular')

    descricao_horario = forms.CharField(label='Horário da Turma',
                                        widget=forms.TextInput(attrs={'placeholder': 'Ex: 24M34'}))

    capacidade_aluno = forms.CharField(label='Vagas', max_length=3,
                                       help_text='Obrigatório. As vagas deve ser menor que a capacidade da sala.')

    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all().order_by('nome'),
                                          label='Departamento', required=False)

    docente = forms.ModelChoiceField(queryset=Docente.objects.all().order_by('nome', 'siape'), label='Docente',
                                     required=False)

    horario_docente = forms.CharField(label='Horário Docente',
                                      widget=forms.TextInput(attrs={'placeholder': 'Ex: 24M34'}),
                                      help_text='Obrigatório. Horário do docente na turma',
                                      required=False)

    ch_docente = forms.CharField(label='CH Docente',
                                 widget=forms.TextInput(attrs={'placeholder': 'Ex: 60'}),
                                 help_text='Obrigatório. Carga horária do docente em horas.',
                                 required=False)

    vinculos_docente = forms.CharField(label='Vínculos Docentes', widget=forms.HiddenInput, required=False)

    def __init__(self, *args, **kwargs):
        estrutura = kwargs.pop('estrutura')
        super(SugestaoTurmaForm, self).__init__(*args, **kwargs)
        self.fields['componente'].queryset = get_cc_by_estrutura(estrutura)
        self.fields['docente'].queryset = Docente.objects.none()

        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['docente'].queryset = \
                    Docente.objects.filter(departamento_id=departamento_id).order_by('nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Docente queryset
        elif self.instance.pk:
            # TODO aqui seria o carregamento de Vínculos Docentes??
            print('forms.py - linha 67')
            # self.fields['docente'].queryset = self.instance.departamento.docente_set.order_by('nome')
            self.fields['docente'].queryset = Docente.objects.none()

    class Meta:
        model = SugestaoTurma
        fields = ['codigo_turma', 'componente', 'descricao_horario', 'local', 'capacidade_aluno']
        widgets = {
            'codigo_turma': forms.TextInput(attrs={'placeholder': '01'}),
        }
        labels = {
            'codigo_turma': 'Código Turma',
        }
