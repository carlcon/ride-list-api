from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, permissions
from .models import Ride
from .serializers import RideSerializer
from main.permissions import IsAdminRole
from main.pagination import StandardResultsSetPagination


class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminRole]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Ride.objects.all()
        
        status = self.request.query_params.get('status')
        rider_email = self.request.query_params.get('rider_email')
        
        filter = Q()
        
        if status:
            filter &= Q(status=status)
        if rider_email:
            filter &= Q(rider__email=rider_email)
            
        return queryset.filter(filter)
            
