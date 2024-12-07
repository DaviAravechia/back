from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Pacientes, Consultas, Medico, CustomUser
from .serializers import PacientesSerializer, ConsultasSerializer, MedicoSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# Pacientes ViewSet
class PacienteViewSet(ModelViewSet):
    queryset = Pacientes.objects.all()
    serializer_class = PacientesSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def consultas(self, request, pk=None):
        """
        Lista todas as consultas associadas a um paciente específico.
        """
        paciente = self.get_object()
        consultas = Consultas.objects.filter(paciente=paciente)
        serializer = ConsultasSerializer(consultas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Médicos ViewSet
class MedicoViewSet(ModelViewSet):
    queryset = Medico.objects.all()
    serializer_class = MedicoSerializer
    permission_classes = [IsAuthenticated]


# Consultas ViewSet
class ConsultaViewSet(ModelViewSet):
    queryset = Consultas.objects.all()
    serializer_class = ConsultasSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['POST'])
    def agendar(self, request):
        """
        Agenda uma nova consulta.
        """
        data = request.data
        try:
            paciente = Pacientes.objects.get(user=request.user)
            medico = Medico.objects.get(uuid=data['medico_uuid'])
            data_hora = data['data_hora']

            # Verifica disponibilidade
            if Consultas.objects.filter(medico=medico, data_hora=data_hora).exists():
                return Response({"error": "O médico não está disponível nesse horário."}, status=status.HTTP_400_BAD_REQUEST)

            consulta = Consultas.objects.create(
                paciente=paciente,
                medico=medico,
                data_hora=data_hora,
                observacoes=data.get('observacoes', '')
            )
            serializer = ConsultasSerializer(consulta)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Pacientes.DoesNotExist:
            return Response({"error": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Medico.DoesNotExist:
            return Response({"error": "Médico não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Funções Individuais
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_paciente(request, id):
    """
    Atualiza parcialmente as informações de um paciente.
    """
    try:
        paciente = Pacientes.objects.get(uuid=id)
        serializer = PacientesSerializer(paciente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Pacientes.DoesNotExist:
        return Response({"error": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_paciente(request, id):
    """
    Exclui um paciente com base no UUID.
    """
    try:
        paciente = Pacientes.objects.get(uuid=id)
        paciente.delete()
        return Response({"message": "Paciente excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
    except Pacientes.DoesNotExist:
        return Response({"error": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Registra um novo usuário.
    """
    try:
        data = request.data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        user.save()
        return Response({"message": "Usuário registrado com sucesso!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_patient(request):
    """
    Registra um novo paciente.
    """
    try:
        data = request.data
        if CustomUser.objects.filter(email=data['email']).exists():
            return Response({"error": "E-mail já registrado."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            is_patient=True
        )
        Pacientes.objects.create(
            user=user,
            nome=data['nome'],
            data_nascimento=data['data_nascimento'],
            telefone=data['telefone'],
            email=data['email'],
            historico_medico=data.get('historico_medico', '')
        )
        return Response({"message": "Paciente registrado com sucesso!"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    """
    Login de usuários com JWT.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'is_patient': getattr(user, 'is_patient', False),
            'is_staff_user': getattr(user, 'is_staff_user', False),
        })
    return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_400_BAD_REQUEST)


def empty_favicon(request):
    """
    Retorna uma resposta vazia para evitar erro 404 ao buscar favicon.
    """
    return HttpResponse("", content_type="image/x-icon")


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancelar_consulta(request, id):
    """
    Cancela uma consulta com base no UUID.
    """
    try:
        consulta = Consultas.objects.get(uuid=id)
        consulta.delete()
        return Response({"message": "Consulta cancelada com sucesso."}, status=status.HTTP_204_NO_CONTENT)
    except Consultas.DoesNotExist:
        return Response({"error": "Consulta não encontrada."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def atualizar_consulta(request, id):
    """
    Atualiza parcialmente as informações de uma consulta.
    """
    try:
        consulta = Consultas.objects.get(uuid=id)
    except Consultas.DoesNotExist:
        return Response({"error": "Consulta não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ConsultasSerializer(consulta, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)