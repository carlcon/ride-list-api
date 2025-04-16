from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Ride
from .serializers import RideSerializer

# Create your views here.

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'driver':
            return Ride.objects.filter(driver=user)
        elif user.role == 'passenger':
            return Ride.objects.filter(rider=user)
        return Ride.objects.all()
