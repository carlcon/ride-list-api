from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from main.permissions import IsAdminRole

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
