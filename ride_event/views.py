from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import RideEvent
from .serializers import RideEventSerializer

# Create your views here.

class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'driver':
            return RideEvent.objects.filter(ride__driver=user)
        elif user.role == 'passenger':
            return RideEvent.objects.filter(ride__rider=user)
        return RideEvent.objects.all()
