from rest_framework import serializers
from .models import Ride
from django.contrib.auth import get_user_model

User = get_user_model()

class RideSerializer(serializers.ModelSerializer):
    rider = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='passenger'))
    driver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='driver'),
        required=False,
        allow_null=True
    )

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
            'pickup_time'
        ]
        read_only_fields = ['id']

    def validate(self, data):
        if data.get('driver') and data['driver'].role != 'driver':
            raise serializers.ValidationError("Driver must have driver role")
        if data['rider'].role != 'passenger':
            raise serializers.ValidationError("Rider must have passenger role")
        return data