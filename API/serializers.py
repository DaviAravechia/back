from rest_framework import serializers
from .models import Pacientes, Consultas
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    # Serializer para criar e gerenciar usuários
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


# class PacientesSerializer(serializers.ModelSerializer):
#     # Relaciona o usuário com o paciente
#     user_id = UserSerializer()

    class Meta:
        model = Pacientes
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user_id')  # Retira os dados do usuário
        user = User.objects.create_user(**user_data)  # Cria o usuário
        paciente = Pacientes.objects.create(user_id=user, **validated_data)  # Cria o paciente
        return paciente


class ConsultasSerializer(serializers.ModelSerializer):
    paciente_nome = serializers.ReadOnlyField(source='paciente.nome')  # Nome do paciente como campo adicional

    class Meta:
        model = Consultas
        fields = '__all__'

