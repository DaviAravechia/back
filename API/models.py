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
<<<<<<< HEAD
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=True, null=True)
    historico_medico = models.TextField(blank=True, null=True)
=======
    telefone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Número de telefone inválido.")]
    )
    historico_medico = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=False)  
    cpf = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^\d{11}$', message="CPF deve conter 11 dígitos.")]
    )

    def __str__(self):
        return self.nome
>>>>>>> 093e4bc21d7e89b8aea182ec193d656fe9dda52f

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

<<<<<<< HEAD
    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"
=======
def empty_favicon(request):
    return HttpResponse("", content_type="image/x-icon")

def api_root(request):
    return JsonResponse({"message": "Bem-vindo à API!"})

>>>>>>> 093e4bc21d7e89b8aea182ec193d656fe9dda52f
