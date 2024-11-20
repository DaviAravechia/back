from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Pacientes(models.Model):
    user_id = models.OneToOneField(
        User,  # Relaciona um paciente ao modelo User
        on_delete=models.CASCADE,  # Exclui o paciente se o usuário for excluído
        related_name='paciente'  # Facilita consultas reversas
    )
    uuid = models.UUIDField(primary_key=True, editable=False)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    telefone = models.IntegerField()
    historico_medico = models.TextField()  # Ajustado para TextField'
    cpf = models.CharField(max_length=11,)


    def __str__(self):
        return self.nome
    
class Consultas(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    data_e_hora_consulta = models.DateTimeField()
    descricao = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('agendada', 'Agendada'),
        ('concluida', 'Concluida'),
        ('cancelada', 'Cancelada')
    ]
)

