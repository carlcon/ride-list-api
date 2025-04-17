from datetime import timedelta
from django.shortcuts import render
from django.db.models import Q, Prefetch
from django.db.models.expressions import RawSQL
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import Ride, RideEvent
from .serializers import RideSerializer, RideEventSerializer
from main.permissions import IsAdminRole
from main.pagination import StandardResultsSetPagination

class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminRole]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if user.role == 'driver':
            return RideEvent.objects.filter(ride__driver=user)
        elif user.role == 'passenger':
            return RideEvent.objects.filter(ride__rider=user)
        return RideEvent.objects.all()

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminRole]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = self.queryset.select_related('rider', 'driver')
        
        status = self.request.query_params.get('status')
        rider_email = self.request.query_params.get('rider_email')
        sort_by = self.request.query_params.get('sort_by')
        order = self.request.query_params.get('order', 'asc')
        lat = self.request.query_params.get('latitude')
        lng = self.request.query_params.get('longitude')
        
        filter = Q()
        
        if status:
            filter &= Q(status=status)
        if rider_email:
            filter &= Q(rider__email=rider_email)
        
        queryset = queryset.filter(filter)
        
        if sort_by == 'pickup_time':
            if order.lower() == 'desc':
                queryset = queryset.order_by('-pickup_time')
            else:
                queryset = queryset.order_by('pickup_time')
        
        elif sort_by == 'distance':
            if not all([lat, lng]):
                raise ValidationError('Both latitude and longitude are required for distance sorting')
            
            distance_sql = """
                point(pickup_longitude, pickup_latitude) <@> point(%s, %s)
            """
            queryset = queryset.annotate(
                distance=RawSQL(distance_sql, (lng, lat))
            ).order_by('distance')        
        
        return queryset