from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Generate monthly trip duration report using raw SQL"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    TO_CHAR(pickup.created_at, 'YYYY-MM') AS month,
                    u.first_name || ' ' || u.last_name AS driver_name,
                    COUNT(*) AS trip_count
                FROM ride_ride r
                JOIN ride_event pickup 
                    ON r.id = pickup.ride_id AND pickup.description = 'Driver arrived at pickup location'
                JOIN ride_event dropoff 
                    ON r.id = dropoff.ride_id AND dropoff.description = 'Arrived at destination'
                JOIN user_user u ON r.driver_id = u.id
                WHERE dropoff.created_at - pickup.created_at > INTERVAL '1 hour'
                GROUP BY month, driver_name
                ORDER BY month, driver_name;
            """)
            rows = cursor.fetchall()

        if not rows:
            self.stdout.write("No qualifying trips found.")
            return

        self.stdout.write("Monthly Report of Trips > 1 Hour:\n")
        for row in rows:
            month, driver_name, count = row
            self.stdout.write(f"{month} - {driver_name}: {count} trip(s)")
