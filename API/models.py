from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Pacientes(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    telefone = PhoneNumberField()
    email = models.EmailField()
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

