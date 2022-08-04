from django.contrib import admin

from core.models import Historico, Horario, Centro, Departamento, Curso, ComponenteCurricular, EstruturaCurricular, \
    OrganizacaoCurricular, Docente, SolicitacaoTurma, Turma, SugestaoTurma, Sala, FuncaoGratificada, Discente, PeriodoLetivo, \
    Enquete, VotoTurma, VinculoDocente, VinculoDocenteSugestao


class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sigla', 'bloco', 'centro', 'campus')


class ComponenteCurricularAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'departamento')
    search_fields = ['codigo','nome']


class EstruturaCurricularAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nome', 'ch_total_minima', 'status')
    search_fields = ['nome']


class OrganizacaoCurricularAdmin(admin.ModelAdmin):
    list_display = ('id_curriculo_componente', 'componente', 'semestre', 'tipo_vinculo')
    list_filter = ['estrutura', 'semestre']
    search_fields = ['id_curriculo_componente']


class DocenteAdmin(admin.ModelAdmin):
    list_display = ('siape', 'nome', 'lotacao', 'usuario')
    list_filter = ['lotacao']
    search_fields = ['siape', 'nome']


class FuncaoGratificadaAdmin(admin.ModelAdmin):
    list_display = ('siape', 'nome', 'lotacao', 'atividade', 'unidade_designacao')
    list_filter = ['atividade']
    search_fields = ['nome', 'atividade']


class DiscenteAdmin(admin.ModelAdmin):
    list_display = ('matricula', 'nome_discente', 'nome_curso', 'nome_unidade', 'status')
    list_filter = ['ano_ingresso', 'periodo_ingresso', 'status', 'nome_curso']
    search_fields = ['matricula', 'nome_discente']

class TurmaAdmin(admin.ModelAdmin):
    list_display = ('codigo_turma', 'componente', 'ano', 'periodo')
    list_filter = ['ano', 'periodo']
    search_fields = ['componente']

class PeriodoLetivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ano', 'periodo', 'data_inicio', 'data_fim', 'status')


class EnqueteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'curso', 'numero_votos', 'periodo', 'data_hora_inicio', 'data_hora_fim', 'status')


class VotoTurmaAdmin(admin.ModelAdmin):
    list_display = ('enquete', 'componente', 'get_matricula', 'get_nome', 'get_email')
    list_filter = ['enquete', 'componente', 'discente__matricula']


    def get_matricula(self, obj):
        return obj.discente.matricula

    get_matricula.admin_order_field  = 'discente__matricula'  #Allows column order sorting
    get_matricula.short_description = 'Matrícula'  #Renames column head

    def get_nome(self, obj):
        return obj.discente.nome_discente

    get_nome.admin_order_field  = 'discente__nome_discente'  #Allows column order sorting
    get_nome.short_description = 'Nome'  #Renames column head

    def get_email(self, obj):
        return obj.discente.usuario.email

    get_email.admin_order_field  = 'discente__usuario__email'  #Allows column order sorting
    get_email.short_description = 'E-mail'  #Renames column head


admin.site.register(Centro)
admin.site.register(Departamento)
admin.site.register(Sala, SalaAdmin)
admin.site.register(ComponenteCurricular, ComponenteCurricularAdmin)
admin.site.register(EstruturaCurricular, EstruturaCurricularAdmin)
admin.site.register(OrganizacaoCurricular, OrganizacaoCurricularAdmin)
admin.site.register(Curso)
admin.site.register(Horario)
admin.site.register(Docente, DocenteAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(SugestaoTurma)
admin.site.register(FuncaoGratificada, FuncaoGratificadaAdmin)
admin.site.register(Discente, DiscenteAdmin)
admin.site.register(PeriodoLetivo, PeriodoLetivoAdmin)
admin.site.register(Enquete, EnqueteAdmin)
admin.site.register(VinculoDocente)
admin.site.register(VinculoDocenteSugestao)
admin.site.register(SolicitacaoTurma)
admin.site.register(Historico)
admin.site.register(VotoTurma, VotoTurmaAdmin)
