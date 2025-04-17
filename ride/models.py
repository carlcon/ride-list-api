from django.db import models
from django.db.models import Index
from django.contrib.auth import get_user_model

User = get_user_model()

class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('en-route', 'En Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_driver', null=True, blank=True)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"Ride {self.id} - {self.status}"
    
    class Meta:
        indexes = [
            models.Index(fields=['pickup_time']),
            models.Index(fields=['pickup_latitude', 'pickup_longitude'])
        ]
