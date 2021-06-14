from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from core.bo.curso import get_curso_by_codigo
from core.bo.curriculo import get_componentes_by_curso, get_componentes_by_curso_semestre, get_semestres_by_curso
from core.bo.enquetes import get_componentes_enquete
from core.bo.sevices import get_cc_by_estrutura, get_estrutura_by_curso
from core.dao.componente_dao import get_componentes_curriculares
from core.models import Discente, Historico, OrganizacaoCurricular, SugestaoTurma, Docente, ComponenteCurricular, Departamento, Sala, \
    VotoTurma


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

    local = forms.ModelChoiceField(queryset=Sala.objects.all().order_by('campus', 'nome'),
                                   label='Local', required=False)
    checked = forms.BooleanField(
        label='Verificar Choques em Optativas', initial=True,required=False)
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


class VotoTurmaForm(ModelForm):
    class Meta:
        model = VotoTurma
        fields = ['componente']

    def __init__(self, *args, **kwargs):
        enquete = kwargs.pop('enquete')
        super(VotoTurmaForm, self).__init__(*args, **kwargs)
        self.fields['componente'].queryset = get_componentes_enquete(enquete)

SEMESTER_CHOICES = (
    ("1", "1º Semestre"),
    ("2", "2º Semestre"),
    ("3", "3º Semestre"),
    ("4", "4º Semestre"),
    ("5", "5º Semestre"),
    ("6", "6º Semestre"),
    ("7", "7º Semestre"),
    ("8", "8º Semestre"),
    ("9", "9º Semestre"),
    ("10", "10º Semestre"),
    ("0", "Optativas"),
)

class HistoricoForm(ModelForm):
    semestre = forms.ChoiceField(choices = SEMESTER_CHOICES, label='Semestre do Curso')
    componente = forms.ModelChoiceField(queryset=ComponenteCurricular.objects.all(), label='Componente Cursado')
    curso = forms.CharField(label='Curso', widget=forms.HiddenInput, required=False)
    discente = forms.ModelChoiceField(queryset=Discente.objects.all(), label='Discente', widget=forms.HiddenInput, required=False)
    class Meta:
        model = Historico
        fields = ['semestre', 'componente', 'curso', 'discente']

    def __init__(self, *args, **kwargs):
        discente = kwargs.pop('discente')
        super(HistoricoForm, self).__init__(*args, **kwargs)
        curso = get_curso_by_codigo(discente.id_curso)
        self.initial['curso'] = discente.id_curso
        self.initial['discente'] = discente
        print(self.data)
        semestre = 1
        if self.data:
            semestre = self.data['semestre']
        self.fields['componente'].queryset = get_componentes_by_curso_semestre(curso=curso, semestre=semestre)
        # self.fields['semestre'].queryset = get_semestres_by_curso(curso)
        # self.fields['componente'].queryset = get_componentes_by_curso(curso=curso)
