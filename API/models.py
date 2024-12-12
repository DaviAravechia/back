from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
import uuid
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_staff_user = models.BooleanField(default=False)

    # Sobrescrevendo os campos para evitar conflitos
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Nome único para evitar conflito
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Nome único para evitar conflito
        blank=True,
    )

class Pacientes(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="paciente")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True, blank=True, null=True)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{11}$',
                message="O CPF deve conter exatamente 11 dígitos numéricos.",
            )
        ],
        verbose_name="CPF"
    )
    historico_medico = models.TextField(max_length=255,blank=True, null=True)


    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"

class Medico(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    nome = models.CharField(max_length=255)
    crm = models.CharField(max_length=20, unique=True)
    telefone = models.CharField(max_length=15)
    especialidade = models.CharField(max_length=100, blank=True, null=True)  # Adicionado campo de especialidade

    class Meta:
        verbose_name = "Médico"
        verbose_name_plural = "Médicos"

class Consultas(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, related_name='consultas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='consultas')
    data_hora = models.DateTimeField()
    descricao = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=50,
        choices=[('agendada', 'Agendada'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada')],
        default='agendada'  # Valor padrão
    )

    class Meta:
        verbose_name = "Consulta"
        verbose_name_plural = "Consultas"


