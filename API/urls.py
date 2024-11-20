from django.urls import path
from .views import register, postpacientes, api_root, empty_favicon

urlpatterns = [
    path('', api_root, name='api_root'),  # Rota base para '/api/'
    path('auth/register/', register, name='register'),  # Registro de usuários
    path('restrito/pacientes/', postpacientes, name='postpacientes'),  # CRUD de pacientes
    path('favicon.ico', empty_favicon, name='favicon'),  # Favicon
]
