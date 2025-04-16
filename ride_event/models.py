from django.db import models
from ride.models import Ride

# Create your models here.
class RideEvent(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name="ride_events")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.id} for Ride {self.ride.id} - {self.description}"

    class Meta:
        db_table = 'ride_event'
        verbose_name = 'Ride Event'
        verbose_name_plural = 'Ride Events'
        ordering = ['-created_at']