import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.http import JsonResponse
from django.http import HttpResponse

class Pacientes(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=True, null=True)
    historico_medico = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Consultas(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, related_name='consultas')
    data_hora = models.DateTimeField()
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('agendada', 'Agendada'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada')])

    def __str__(self):
        return f"{self.paciente.nome} - {self.data_hora}"

class Medico(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    nome = models.CharField(max_length=255)
    crm = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome

