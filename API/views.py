from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer
from .models import Pacientes
from django.http import JsonResponse, HttpResponse


@swagger_auto_schema(
    methods=['POST'],
    request_body=UserSerializer,
    tags=['token'],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    View para registrar um novo usuário.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"username": serializer.data["username"]},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @swagger_auto_schema(
#     methods=['POST'],
#     request_body=PacientesSerializer,
#     tags=['pacientes'],
# )
@api_view(['POST'])
@permission_classes([AllowAny])
def postpacientes(request):
    """
    View para criar um novo paciente associado a um usuário.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        paciente = serializer.save()
        return Response(
            # {"id": paciente.uuid, "nome": paciente.nome},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def api_root(request):
    """
    View para exibir a mensagem inicial da API.
    """
    return JsonResponse({"message": "Bem-vindo à API!"})


def empty_favicon(request):
    """
    View para evitar erro 404 ao buscar favicon.
    """
    return HttpResponse("", content_type="image/x-icon")
