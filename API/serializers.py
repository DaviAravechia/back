from rest_framework import serializers
<<<<<<< HEAD
from .models import Pacientes, Consultas, Medico
=======
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


class PacientesSerializer(serializers.ModelSerializer):
    # Relaciona o usuário com o paciente
    user_id = UserSerializer()
>>>>>>> 093e4bc21d7e89b8aea182ec193d656fe9dda52f

class PacientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pacientes
        fields = '__all__'

class ConsultasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultas
        fields = '__all__'

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'
