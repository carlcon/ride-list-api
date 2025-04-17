from django.utils import timezone
import os
import django
import random
from datetime import timedelta
from faker import Faker

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()

from user.models import User
from ride.models import Ride, RideEvent

fake = Faker()

def create_users(num_users=100):
    """Create users with different roles"""
    print("Creating users...")
    users = {
        'admin': [],
        'driver': [],
        'passenger': []
    }
    
    # Create admins (10% of users)
    for _ in range(int(num_users * 0.1)):
        user = User.objects.create_user(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password='password123',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role='admin',
            phone_number="+1" + "".join([str(random.randint(0, 9)) for _ in range(10)])
        )
        users['admin'].append(user)
    
    # Create drivers (30% of users)
    for _ in range(int(num_users * 0.3)):
        user = User.objects.create_user(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password='password123',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role='driver',
            phone_number="+1" + "".join([str(random.randint(0, 9)) for _ in range(10)])
        )
        users['driver'].append(user)
    
    # Create passengers (60% of users)
    for _ in range(int(num_users * 0.6)):
        user = User.objects.create_user(
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            password='password123',
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role='passenger',
            phone_number="+1" + "".join([str(random.randint(0, 9)) for _ in range(10)])
        )
        users['passenger'].append(user)
    
    return users

def create_rides(users, num_rides=10000):
    """Create rides with realistic statuses"""
    print("Creating rides...")
    rides = []
    
    for _ in range(num_rides):
        passenger = random.choice(users['passenger'])
        driver = random.choice(users['driver']) if random.random() > 0.2 else None
        status = random.choice(['requested', 'accepted', 'en-route', 'pickup', 'dropoff', 'completed', 'cancelled'])
        
        pickup_time = timezone.now() - timedelta(days=random.randint(0, 30))
        
        ride = Ride.objects.create(
            status=status,
            rider=passenger,
            driver=driver,
            pickup_latitude=float(fake.latitude()),
            pickup_longitude=float(fake.longitude()),
            dropoff_latitude=float(fake.latitude()),
            dropoff_longitude=float(fake.longitude()),
            pickup_time=pickup_time
        )
        rides.append(ride)
    
    return rides

def create_ride_events(rides, num_events=10000):
    """Create ride events for rides"""
    print("Creating ride events...")
    events = []
    
    status_descriptions = {
        'requested': 'Ride requested by passenger',
        'accepted': 'Driver accepted the ride',
        'en-route': 'Driver is en route to pickup location',
        'pickup': 'Driver arrived at pickup location',
        'dropoff': 'Arrived at destination',
        'completed': 'Ride completed successfully',
        'cancelled': 'Ride was cancelled'
    }
    
    for _ in range(num_events):
        ride = random.choice(rides)
        description = status_descriptions.get(ride.status, 'Status updated')
        
        event = RideEvent.objects.create(
            ride=ride,
            description=description
        )
        events.append(event)
    
    return events

if __name__ == '__main__':
    # Clear existing data
    print("Clearing existing data...")
    RideEvent.objects.all().delete()
    Ride.objects.all().delete()
    User.objects.exclude(is_superuser=True).delete()
    
    # Create new data
    users = create_users(100)  # Create 100 users
    rides = create_rides(users, 10000)  # Create 10,000 rides
    events = create_ride_events(rides, 10000)  # Create 10,000 events
    
    print("Data population complete!")
    print(f"Created {User.objects.count()} users")
    print(f"Created {Ride.objects.count()} rides")
    print(f"Created {RideEvent.objects.count()} events")