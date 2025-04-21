import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import timedelta
from django.utils import timezone
from ride.models import Ride, RideEvent
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username='admin1', password='pass', is_staff=True, role='admin', email='admin@example.com'
    )

@pytest.fixture
def authenticated_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def rider(db):
    return User.objects.create_user(
        username='rider1', email='rider@example.com', first_name='Test Rider', role='passenger', password='pass'
    )

@pytest.fixture
def driver(db):
    return User.objects.create_user(
        username='driver1', email='driver@example.com', first_name='Test Driver', role='driver', password='pass'
    )

@pytest.fixture
def rides(db, rider, driver):
    now = timezone.now()
    rides = [
        Ride.objects.create(
            rider=rider,
            driver=driver,
            pickup_latitude=10.0,
            pickup_longitude=20.0,
            dropoff_latitude=11.0,
            dropoff_longitude=21.0,
            pickup_time=now + timedelta(hours=1),
            status='scheduled'
        ),
        Ride.objects.create(
            rider=rider,
            driver=driver,
            pickup_latitude=11.0,
            pickup_longitude=21.0,
            dropoff_latitude=12.0,
            dropoff_longitude=22.0,
            pickup_time=now + timedelta(hours=2),
            status='completed'
        )
    ]
    for ride in rides:
        RideEvent.objects.create(
            ride=ride,
            description='Ride started',
            created_at=now - timedelta(hours=2)
        )
    return rides

@pytest.mark.django_db
def test_filter_by_status(authenticated_client, rides):
    """Test filtering by ride status"""
    url = reverse('ride-list')
    response = authenticated_client.get(url, {'status': 'scheduled'})
    assert response.status_code == status.HTTP_200_OK
    results = response.data['results']
    assert len(results) == 1
    assert results[0]['status'] == 'scheduled'

@pytest.mark.django_db
def test_filter_by_rider_email(authenticated_client, rides):
    """Test filtering by rider email"""
    url = reverse('ride-list')
    response = authenticated_client.get(url, {'rider_email': 'rider@example.com'})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2

@pytest.mark.django_db
def test_sort_by_pickup_time_desc(authenticated_client, rides):
    """Test sorting by pickup_time in descending order"""
    url = reverse('ride-list')
    response = authenticated_client.get(url, {'sort_by': 'pickup_time', 'order': 'desc'})
    assert response.status_code == status.HTTP_200_OK
    pickup_times = [r['pickup_time'] for r in response.data['results']]
    assert pickup_times == sorted(pickup_times, reverse=True)

@pytest.mark.django_db
def test_distance_sorting_requires_coords(authenticated_client):
    """Test that missing lat/lng when sorting by distance raises error"""
    url = reverse('ride-list')
    response = authenticated_client.get(url, {'sort_by': 'distance'})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert any('both latitude and longitude' in str(error).lower() for error in response.data)

@pytest.mark.django_db
def test_sort_by_distance(authenticated_client, rides):
    """Test sorting by distance from a given point"""
    url = reverse('ride-list')
    response = authenticated_client.get(url, {
        'sort_by': 'distance',
        'latitude': 10.0,
        'longitude': 20.0
    })
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2
    assert 'distance' in response.data['results'][0]

@pytest.mark.django_db
def test_ride_event_list(authenticated_client, rides):
    """Test RideEventViewSet returns ride events"""
    url = reverse('ride_event-list')
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2
