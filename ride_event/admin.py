from django.contrib import admin
from .models import RideEvent

@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'ride', 'created_at']
    list_filter = ['created_at']
    search_fields = ['ride__driver__username', 'ride__rider__username']
    date_hierarchy = 'created_at'
    
    readonly_fields = ['created_at']
    