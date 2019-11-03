from django.contrib import admin

from core.models import Horario, Centro, Departamento, Curso, ComponenteCurricular, EstruturaCurricular, \
    OrganizacaoCurricular

admin.site.register(Centro)
admin.site.register(Departamento)
admin.site.register(ComponenteCurricular)
admin.site.register(EstruturaCurricular)
admin.site.register(OrganizacaoCurricular)
admin.site.register(Curso)
admin.site.register(Horario)
