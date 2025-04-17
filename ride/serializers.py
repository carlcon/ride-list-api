from rest_framework import serializers
from .models import Ride, RideEvent
from django.contrib.auth import get_user_model

User = get_user_model()

class RideEventSerializer(serializers.ModelSerializer):
    ride = serializers.HyperlinkedRelatedField(
        view_name='ride-detail',
        read_only=True
    )
    
    class Meta:
        model = RideEvent
        fields = ['id', 'ride', 'description', 'created_at']
        read_only_fields = ['id', 'created_at'] 
        extra_kwargs = {
            'url': {'view_name': 'rideevent-detail'}
        }

class RideSerializer(serializers.ModelSerializer):
    rider = serializers.SerializerMethodField()
    driver = serializers.SerializerMethodField()
    todays_ride_events = RideEventSerializer(many=True, read_only=True)

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
        read_only_fields = ['id']
        extra_kwargs = {
            'url': {'view_name': 'ride-detail'}
        }

    def validate(self, data):
        if data.get('driver') and data['driver'].role != 'driver':
            raise serializers.ValidationError("Driver must have driver role")
        if data['rider'].role != 'passenger':
            raise serializers.ValidationError("Rider must have passenger role")
        return data
    
    def get_rider(self, obj):
        return {
            'id': obj.rider.id,
            'email': obj.rider.email,
            'full_name': f"{obj.rider.first_name} {obj.rider.last_name}"
        }

    def get_driver(self, obj):
        if obj.driver:
            return {
                'id': obj.driver.id,
                'email': obj.driver.email,
                'full_name': f"{obj.driver.first_name} {obj.driver.last_name}"
            }
        return None