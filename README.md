# Ride Share API

A RESTful API using Django REST Framework for managing ride information.

## Features

- User Management
- Ride Creation and Listing
- Database setup and population scripts


## Getting Started

### Prerequisites

- Python 3.12
- psql 17.4

### Installation


```bash
# Clone the repository

git clone https://github.com/carlcon/ride-list-api.git
cd ride-list-api

# Create and activate the virtual environment:
pyhon -m venv venv
source venv/bin/activate # for linux. On Windows, use venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from .env.sample (included the default values for easy setup of local db)
cp .env.sample .env

# Setup the database
bash setup_db.sh

# Create a Django superuser 
python manage.py createsuperuser --username admin --email admin@example.com
# When prompted, enter your password (e.g. Admin1234@ )

# Populate the database with sample data:
python populate_db.py

# Create a superuser
python manage.py 

# Start the django's development server.
python manage.py runserver

```