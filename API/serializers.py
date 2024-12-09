from rest_framework import serializers
from .models import Pacientes, Medico, Consultas

class PacientesSerializer(serializers.ModelSerializer):
    total_consultas = serializers.IntegerField(source='consultas.count', read_only=True)

    class Meta:
        model = Pacientes
        fields = ['uuid', 'nome', 'data_nascimento', 'telefone', 'email', 'cpf', 'user', 'total_consultas']

        
class MedicoSerializer(serializers.ModelSerializer):
    crm = serializers.CharField(
        max_length=20,
        error_messages={'blank': 'O CRM não pode estar em branco.'}
    )

    class Meta:
        model = Medico
        fields = ['uuid', 'nome', 'crm', 'telefone', 'especialidade']


class CustomDateTimeField(serializers.DateTimeField):
    def to_representation(self, value):
        return value.strftime('%d/%m/%Y %H:%M')

    def to_internal_value(self, data):
        return super().to_internal_value(data)


class ConsultasSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.CharField(source='paciente.nome', read_only=True)
    medico_nome = serializers.CharField(source='medico.nome', read_only=True)
    data_hora = CustomDateTimeField()

    class Meta:
        model = Consultas
        fields = '__all__'
