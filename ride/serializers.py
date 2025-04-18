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
    rider = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()
    todays_ride_events = serializers.SerializerMethodField()

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
        ]
    
    def get_rider(self, obj):
        return obj.rider.get_full_name()

    def get_driver(self, obj):
        if obj.driver:
            return obj.driver.get_full_name()
        return None
    
    def get_todays_ride_events(self ,obj):
        return RideEventSerializer(obj.todays_ride_events, many=True).data
        