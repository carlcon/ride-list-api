from rest_framework.routers import DefaultRouter
from .views import RideViewSet, RideEventViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'ride_events', RideEventViewSet, basename='ride_event')

urlpatterns = router.urls