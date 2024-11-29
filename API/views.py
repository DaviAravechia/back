from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Pacientes, Consultas
from .serializers import PacientesSerializer, ConsultasSerializer, MedicoSerializer

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_paciente(request, id):
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
    try:
        paciente = Pacientes.objects.get(uuid=id)
        paciente.delete()
        return Response({"message": "Paciente excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
    except Pacientes.DoesNotExist:
        return Response({"error": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agendar_consulta(request):
    serializer = ConsultasSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def atualizar_consulta(request, id):
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
    try:
        consulta = Consultas.objects.get(uuid=id)
        consulta.delete()
        return Response({"message": "Consulta cancelada com sucesso."}, status=status.HTTP_204_NO_CONTENT)
    except Consultas.DoesNotExist:
        return Response({"error": "Consulta não encontrada."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_medico(request):
    serializer = MedicoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_paciente(request):
    serializer = PacientesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pacientes(request):
    """
    Lista todos os pacientes cadastrados.
    """
    pacientes = Pacientes.objects.all()  # Busca todos os pacientes
    serializer = PacientesSerializer(pacientes, many=True)  # Serializa os dados
    return Response(serializer.data)  # Retorna a lista de pacientes

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_consultas_by_paciente(request, paciente_id):
    """
    Lista todas as consultas de um paciente específico.
    """
    try:
        consultas = Consultas.objects.filter(paciente__uuid=paciente_id)
        serializer = ConsultasSerializer(consultas, many=True)
        return Response(serializer.data, status=200)
    except Pacientes.DoesNotExist:
        return Response({"error": "Paciente não encontrado."}, status=404)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_consulta(request, paciente_id):
    """
    Cria uma nova consulta para um paciente.
    """
    try:
        paciente = Pacientes.objects.get(uuid=paciente_id)
        consulta_data = request.data
        consulta_data['paciente'] = paciente.id
        serializer = ConsultasSerializer(data=consulta_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    except Pacientes.DoesNotExist:
        return Response({"error": "Paciente não encontrado."}, status=404)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_consulta(request, id):
    """
    Atualiza uma consulta pelo UUID.
    """
    try:
        consulta = Consultas.objects.get(uuid=id)
    except Consultas.DoesNotExist:
        return Response({"error": "Consulta não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ConsultasSerializer(consulta, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_consulta(request, id):
    """
    Exclui uma consulta pelo UUID.
    """
    try:
        consulta = Consultas.objects.get(uuid=id)
        consulta.delete()
        return Response({"message": "Consulta excluída com sucesso."}, status=status.HTTP_204_NO_CONTENT)
    except Consultas.DoesNotExist:
        return Response({"error": "Consulta não encontrada."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def listar_consultas_por_paciente(request, paciente_id):
    """
    Lista todas as consultas de um paciente específico.
    """
    consultas = Consultas.objects.filter(paciente_id=paciente_id)
    serializer = ConsultasSerializer(consultas, many=True)
    return Response(serializer.data)

def empty_favicon(request):
    """
    View para evitar erro 404 ao buscar favicon.
    
    """
    return HttpResponse("", content_type="image/x-icon")