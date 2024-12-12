from django.contrib import admin
from .models import Medico, Pacientes,Consultas

admin.site.register(Pacientes)
admin.site.register(Medico)
admin.site.register(Consultas)