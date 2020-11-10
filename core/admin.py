from django.contrib import admin

from core.models import Horario, Centro, Departamento, Curso, ComponenteCurricular, EstruturaCurricular, \
    OrganizacaoCurricular, Docente, SolicitacaoTurma, Turma, SugestaoTurma, Sala, FuncaoGratificada, Discente, PeriodoLetivo, \
    Enquete, VotoTurma, VinculoDocente, VinculoDocenteSugestao

admin.site.register(Centro)
admin.site.register(Departamento)


class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'bloco', 'centro', 'campus')


admin.site.register(Sala, SalaAdmin)


class ComponenteCurricularAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'departamento')
    search_fields = ['nome']


admin.site.register(ComponenteCurricular, ComponenteCurricularAdmin)
admin.site.register(EstruturaCurricular)


class OrganizacaoCurricularAdmin(admin.ModelAdmin):
    list_display = ('id_curriculo_componente', 'componente', 'semestre', 'tipo_vinculo')
    list_filter = ['estrutura', 'semestre']
    search_fields = ['id_curriculo_componente']


admin.site.register(OrganizacaoCurricular, OrganizacaoCurricularAdmin)
admin.site.register(Curso)
admin.site.register(Horario)


class DocenteAdmin(admin.ModelAdmin):
    list_display = ('siape', 'nome', 'lotacao', 'usuario')
    list_filter = ['lotacao']
    search_fields = ['siape', 'nome']


admin.site.register(Docente, DocenteAdmin)
admin.site.register(Turma)
admin.site.register(SugestaoTurma)


class FuncaoGratificadaAdmin(admin.ModelAdmin):
    list_display = ('siape', 'nome', 'lotacao', 'atividade', 'unidade_designacao')
    list_filter = ['atividade']
    search_fields = ['nome', 'atividade']


admin.site.register(FuncaoGratificada, FuncaoGratificadaAdmin)


class DiscenteAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome_discente', 'nome_curso', 'nome_unidade', 'status')
    list_filter = ['ano_ingresso', 'periodo_ingresso', 'status']
    search_fields = ['nome_discente']


admin.site.register(Discente, DiscenteAdmin)


class PeriodoLetivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano', 'periodo', 'data_inicio', 'data_fim', 'status')


admin.site.register(PeriodoLetivo, PeriodoLetivoAdmin)


class EnqueteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso', 'numero_votos', 'periodo', 'data_hora_inicio', 'data_hora_fim', 'status')


admin.site.register(Enquete, EnqueteAdmin)
admin.site.register(VotoTurma)
admin.site.register(VinculoDocente)
admin.site.register(VinculoDocenteSugestao)
admin.site.register(SolicitacaoTurma)
