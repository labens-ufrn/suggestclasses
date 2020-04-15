from django.contrib import admin

from core.models import Horario, Centro, Departamento, Curso, ComponenteCurricular, EstruturaCurricular, \
    OrganizacaoCurricular, Docente, Turma, SugestaoTurma, Sala, FuncaoGratificada, Discente

admin.site.register(Centro)
admin.site.register(Departamento)
admin.site.register(ComponenteCurricular)
admin.site.register(EstruturaCurricular)
admin.site.register(OrganizacaoCurricular)
admin.site.register(Curso)
admin.site.register(Horario)


class DocenteAdmin(admin.ModelAdmin):
    list_display = ('siape', 'nome', 'lotacao', 'usuario')
    list_filter = ['lotacao']
    search_fields = ['siape', 'nome']


admin.site.register(Docente, DocenteAdmin)
admin.site.register(Turma)
admin.site.register(SugestaoTurma)
admin.site.register(Sala)


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
