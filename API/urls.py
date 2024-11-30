from django.urls import path
<<<<<<< HEAD
from .views import (
    create_paciente, list_pacientes, update_paciente, delete_paciente,
    agendar_consulta, listar_consultas_por_paciente,register_user
)

urlpatterns = [
    # Pacientes
    path('paciente/', list_pacientes, name='list_pacientes'),
    path('paciente/create/', create_paciente, name='create_paciente'),
    path('paciente/<uuid:id>/', update_paciente, name='update_paciente'),
    path('paciente/<uuid:id>/delete/', delete_paciente, name='delete_paciente'),
    path('auth/novo/', register_user, name='register_user'),

    # Consultas
    path('paciente/<uuid:paciente_id>/consultas/', listar_consultas_por_paciente, name='listar_consultas_por_paciente'),
    path('consulta/', agendar_consulta, name='agendar_consulta'),
=======
from .views import login, register, PacientesListCreateView, PacienteDetailView

urlpatterns = [
    path('auth/login/', login, name='login'),
    path('auth/register/', register, name='register'),
    path('pacientes/', PacientesListCreateView.as_view(), name='pacientes_list_create'),
    path('pacientes/<int:id>/', PacienteDetailView.as_view(), name='paciente_detail'),
>>>>>>> 093e4bc21d7e89b8aea182ec193d656fe9dda52f
]