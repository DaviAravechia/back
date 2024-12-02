from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PacienteViewSet, ConsultaViewSet, MedicoViewSet,
    register_user, update_paciente, delete_paciente,
    atualizar_consulta, cancelar_consulta, empty_favicon  # Import correto
)

# Roteador do DRF
router = DefaultRouter()
router.register(r'pacientes', PacienteViewSet, basename='pacientes')
router.register(r'consultas', ConsultaViewSet, basename='consultas')
router.register(r'medicos', MedicoViewSet, basename='medicos')  # Rota para médicos

urlpatterns = [
    # Rotas automáticas
    path('', include(router.urls)),

    # Funções individuais
    path('pacientes/<uuid:id>/update/', update_paciente, name='update_paciente'),
    path('pacientes/<uuid:id>/delete/', delete_paciente, name='delete_paciente'),
    path('consultas/<uuid:id>/update/', atualizar_consulta, name='atualizar_consulta'),
    path('consultas/<uuid:id>/cancel/', cancelar_consulta, name='cancelar_consulta'),

    # Registro de usuário
    path('auth/novo/', register_user, name='register_user'),

    # Favicon
    path('favicon.ico', empty_favicon, name='empty_favicon'),
]
