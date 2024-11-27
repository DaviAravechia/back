from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
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
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"username": serializer.data["username"]},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


def empty_favicon(request):
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
