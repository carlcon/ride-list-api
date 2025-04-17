from django.contrib import admin
from .models import Ride, RideEvent

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['id', 'driver', 'rider', 'status', 'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude', 'pickup_time']
    list_filter = ['status']
    search_fields = ['driver__username', 'rider__username']

@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'ride', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['ride__driver__username', 'ride__rider__username']
    date_hierarchy = 'created_at'
    
    readonly_fields = ['created_at']