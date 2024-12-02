from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Pacientes, Consultas, Medico
from .serializers import PacientesSerializer, ConsultasSerializer, MedicoSerializer


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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Funções Individuais
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_paciente(request, id):
    """
    Atualiza parcialmente as informações de um paciente.
    """
    try:
        paciente = Pacientes.objects.get(uuid=id)
    except Pacientes.DoesNotExist:
        return Response({"error": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    serializer = PacientesSerializer(paciente, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


def empty_favicon(request):
    """
    Retorna uma resposta vazia para evitar erro 404 ao buscar favicon.
    """
    return HttpResponse("", content_type="image/x-icon")


def create(self, request, *args, **kwargs):
    print("Dados recebidos no back-end:", request.data)
    serializer = self.get_serializer(data=request.data)
    if not serializer.is_valid():
        print("Erros na validação:", serializer.errors)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
