from rest_framework import serializers
from .models import Pacientes, Consultas

class PacientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacientes
        fields = '_all_'

class Meta:
    model = Pacientes
    fields = ('username', 'password')

    def create(self, validated_data):
        pacientes = Pacientes(**validated_data)
        pacientes.set_password(validated_data['password'])
        pacientes.save()
        return pacientes