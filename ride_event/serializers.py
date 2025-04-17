from rest_framework import serializers
from .models import RideEvent

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