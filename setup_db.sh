#!/bin/bash

# Create database
createdb ride_share_db

# Create user if not exists
psql -U postgres -c "CREATE USER postgres WITH PASSWORD 'postgres';" || true

# Grant privileges
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ride_share_db TO postgres;"

echo "Database setup completed!" 