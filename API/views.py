from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
<<<<<<< HEAD
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Pacientes, Consultas, Medico
from .serializers import PacientesSerializer, ConsultasSerializer, MedicoSerializer

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_paciente(request, id):
    try:
        paciente = Pacientes.objects.get(uuid=id)
    except Pacientes.DoesNotExist:
        return Response({"error": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = PacientesSerializer(paciente, data=request.data, partial=True)
=======
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from .models import Pacientes, Consultas
from .serializers import UserSerializer, PacientesSerializer, ConsultasSerializer


def get_tokens_for_user(user):
    """
    Gera tokens JWT para um usuário autenticado.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nome do usuário'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Senha do usuário'),
        }
    ),
    responses={200: "Login bem-sucedido!", 401: "Credenciais inválidas."}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Os campos 'username' e 'password' são obrigatórios."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        tokens = get_tokens_for_user(user)
        return Response(
            {"message": "Login bem-sucedido!", "tokens": tokens, "username": username},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"error": "Credenciais inválidas ou usuário inativo."},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={201: "Usuário criado com sucesso!", 400: "Erro de validação."}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if User.objects.filter(username=request.data.get("username")).exists():
        return Response(
            {"error": "Usuário já existe."},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = UserSerializer(data=request.data)
>>>>>>> 093e4bc21d7e89b8aea182ec193d656fe9dda52f
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

<<<<<<< HEAD
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
=======
class PacientesListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pacientes = Pacientes.objects.filter(user_id=request.user)  # Retorna apenas pacientes do usuário autenticado
        serializer = PacientesSerializer(pacientes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user_id'] = request.user.id  # Adiciona o usuário autenticado automaticamente
        serializer = PacientesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PacienteDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            paciente = Pacientes.objects.get(id=id, user_id=request.user)  # Garante que o paciente pertence ao usuário
            serializer = PacientesSerializer(paciente)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Pacientes.DoesNotExist:
            return Response({"error": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            paciente = Pacientes.objects.get(id=id, user_id=request.user)  # Garante que o paciente pertence ao usuário
            serializer = PacientesSerializer(paciente, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Pacientes.DoesNotExist:
            return Response({"error": "Paciente não encontrado."}, status=status.HTTP_404_NOT_FOUND)


def api_root(request):
    return JsonResponse({"message": "Bem-vindo à API!"})
>>>>>>> 093e4bc21d7e89b8aea182ec193d656fe9dda52f




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
<<<<<<< HEAD
    """
    View para evitar erro 404 ao buscar favicon.
    
    """
    return HttpResponse("", content_type="image/x-icon")
=======
    return HttpResponse("", content_type="image/x-icon")


class ConsultasListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        consultas = Consultas.objects.filter(paciente__user_id=request.user)  # Consultas de pacientes do usuário autenticado
        serializer = ConsultasSerializer(consultas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ConsultasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConsultasDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            consulta = Consultas.objects.get(id=id, paciente__user_id=request.user)  # Garante que a consulta pertence ao usuário
            serializer = ConsultasSerializer(consulta)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Consultas.DoesNotExist:
            return Response({"error": "Consulta não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            consulta = Consultas.objects.get(id=id, paciente__user_id=request.user)  # Garante que a consulta pertence ao usuário
            serializer = ConsultasSerializer(consulta, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Consultas.DoesNotExist:
            return Response({"error": "Consulta não encontrada."}, status=status.HTTP_404_NOT_FOUND)
>>>>>>> 093e4bc21d7e89b8aea182ec193d656fe9dda52f
