from django.urls import path
from .views import login, register, PacientesListCreateView, PacienteDetailView

urlpatterns = [
    path('auth/login/', login, name='login'),
    path('auth/register/', register, name='register'),
    path('pacientes/', PacientesListCreateView.as_view(), name='pacientes_list_create'),
    path('pacientes/<int:id>/', PacienteDetailView.as_view(), name='paciente_detail'),
]