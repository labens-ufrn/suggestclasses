from django.contrib import admin

from .models import Horario, Centro, Departamento, Curso, ComponenteCurricular

admin.site.register(Centro)
admin.site.register(Departamento)
admin.site.register(ComponenteCurricular)
admin.site.register(Curso)
admin.site.register(Horario)
