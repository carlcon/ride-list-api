from rest_framework.routers import DefaultRouter
from .views import RideEventViewSet

router = DefaultRouter()
router.register(r'ride_events', RideEventViewSet, basename='ride_event')

urlpatterns = router.urls