import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.http import JsonResponse
from django.http import HttpResponse

class Pacientes(models.Model):
    user_id = models.OneToOneField(
        User,  # Relaciona um paciente ao modelo User
        on_delete=models.CASCADE,  # Exclui o paciente se o usuário for excluído
        related_name='paciente'  # Facilita consultas reversas
    )
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    telefone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Número de telefone inválido.")]
    )
    historico_medico = models.TextField(blank=True, null=True)  # Opcional
    cpf = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^\d{11}$', message="CPF deve conter 11 dígitos.")]
    )

    def __str__(self):
        return self.nome

class Medico(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    nome = models.CharField(max_length=255)
    crm = models.CharField(max_length=7)
    telefone = models.CharField(
        max_length=15, 
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', message="Número de telefone inválido.")]
    )
    email = models.EmailField(max_length=254)
    especialidade = models.CharField(max_length=100)
    data_nascimento = models.DateField()


class Consultas(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    data_e_hora_consulta = models.DateTimeField()
    descricao = models.TextField(blank=True, null=True)  # Opcional
    status = models.CharField(
        max_length=20,
        choices=[
            ('agendada', 'Agendada'),
            ('concluida', 'Concluída'),
            ('cancelada', 'Cancelada')
        ],
        default='agendada'
    )

    def __str__(self):
        return f"Consulta de {self.paciente.nome} em {self.data_e_hora_consulta}"


def empty_favicon(request):
    return HttpResponse("", content_type="image/x-icon")

def api_root(request):
    return JsonResponse({"message": "Bem-vindo à API!"})