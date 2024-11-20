from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes

# Create your views here.

# @api_view(['POST'])
# def paciente_

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer
from .serializers import PacientesSerializer


@swagger_auto_schema(
    methods=['POST'],
    request_body=UserSerializer,
    tags=['token'],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"username": serializer.data["username"]}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def postpacientes(request):
    serializer = UserSerializer.PacientesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response( status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)