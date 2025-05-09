from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from .serializers import UserSerializer
from main.permissions import IsAdminRole
from main.pagination import StandardResultsSetPagination

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    pagination_class = StandardResultsSetPagination
