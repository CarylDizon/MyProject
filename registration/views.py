from django.shortcuts import render
from .models import UserRegistration
from .serializer import RegistrationSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_user(request):
    users = UserRegistration.objects.all()
    serializer = RegistrationSerializer(users, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)