from django.urls import path
from .views import (
    create_paciente, list_pacientes, update_paciente, delete_paciente,
    agendar_consulta, listar_consultas_por_paciente
)

urlpatterns = [
    # Pacientes
    path('paciente/', list_pacientes, name='list_pacientes'),
    path('paciente/create/', create_paciente, name='create_paciente'),
    path('paciente/<uuid:id>/', update_paciente, name='update_paciente'),
    path('paciente/<uuid:id>/delete/', delete_paciente, name='delete_paciente'),

    # Consultas
    path('paciente/<uuid:paciente_id>/consultas/', listar_consultas_por_paciente, name='listar_consultas_por_paciente'),
    path('consulta/', agendar_consulta, name='agendar_consulta'),
]