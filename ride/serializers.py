from rest_framework import serializers
from .models import Ride, RideEvent
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class RideEventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RideEvent
        fields = ['id', 'description', 'created_at']


class RideSerializer(serializers.ModelSerializer):
    rider = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='passenger'), style={'base_template': 'input.html'})
    driver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='driver'),
        required=False,
        allow_null=True,
        style={'base_template': 'input.html'}
    )
    todays_ride_events = serializers.SerializerMethodField()
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            'id', 
            'status', 
            'rider', 
            'driver',
            'pickup_latitude', 
            'pickup_longitude',
            'dropoff_latitude', 
            'dropoff_longitude',
            'pickup_time',
            'todays_ride_events',
            'distance',
        ]
    
    def get_todays_ride_events(self ,obj):
        todays_ride = obj.todays_ride_events if hasattr(obj, 'todays_ride_events') else []
        return RideEventSerializer(todays_ride, many=True).data
    
    def get_distance(self, obj):
        distance = obj.distance if hasattr(obj, 'distance') else None
        return distance