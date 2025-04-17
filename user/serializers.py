from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    rides_as_rider = serializers.HyperlinkedRelatedField(
        view_name='ride-detail',
        many=True,
        read_only=True
    )
    rides_as_driver = serializers.HyperlinkedRelatedField(
        view_name='ride-detail',
        many=True,
        read_only=True
    )
    
    class Meta:
        model = User
        fields = [
            'id', 
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'role', 
            'phone_number',
            'rides_as_rider',
            'rides_as_driver',
        ]
        read_only_fields = ['id']
        extra_kwargs = {
            'url': {'view_name': 'user-detail'},
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user 