from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Paciente(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    telefone = PhoneNumberField()
    email = models.EmailField()
    historico_medico = models.TextField()  # Ajustado para TextField
    cpf = models.CharField(max_length=11,)


    def __str__(self):
        return self.nome


