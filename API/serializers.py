from rest_framework import serializers
from .models import Pacientes, Medico, Consultas

class PacientesSerializer(serializers.ModelSerializer):
    total_consultas = serializers.IntegerField(source='consultas.count', read_only=True)

    class Meta:
        model = Pacientes
        fields = ['uuid', 'nome', 'data_nascimento', 'telefone', 'email', 'historico_medico', 'user', 'total_consultas']  # Inclua 'total_consultas' aqui


class MedicoSerializer(serializers.ModelSerializer):
    crm = serializers.RegexField(
        regex=r'^\d{4,6}-[A-Za-z]{2}$',
        error_messages={'invalid': 'O CRM deve seguir o formato 123456-XX.'}
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
