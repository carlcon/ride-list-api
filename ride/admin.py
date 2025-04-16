from django.contrib import admin
from .models import Ride

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ['id', 'driver', 'rider', 'status']
    list_filter = ['status']
    search_fields = ['driver__username', 'rider__username']