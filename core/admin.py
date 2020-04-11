from django.contrib import admin

from core.models import Horario, Centro, Departamento, Curso, ComponenteCurricular, EstruturaCurricular, \
    OrganizacaoCurricular, Docente, Turma, SugestaoTurma, Sala, FuncaoGratificada

admin.site.register(Centro)
admin.site.register(Departamento)
admin.site.register(ComponenteCurricular)
admin.site.register(EstruturaCurricular)
admin.site.register(OrganizacaoCurricular)
admin.site.register(Curso)
admin.site.register(Horario)
admin.site.register(Docente)
admin.site.register(Turma)
admin.site.register(SugestaoTurma)
admin.site.register(Sala)
admin.site.register(FuncaoGratificada)
