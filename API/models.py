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

    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

class Consultas(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, related_name='consultas')
    data_hora = models.DateTimeField()
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('agendada', 'Agendada'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada')])

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"

class Medico(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    nome = models.CharField(max_length=255)
    crm = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=15)

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
