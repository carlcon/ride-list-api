# Ride List API

A RESTful API using Django REST Framework for managing ride information.


## Features

- User Management
- Ride Creation and Listing
- Database setup and population scripts


## Getting Started

Clone the repository
```bash
git clone https://github.com/carlcon/ride-list-api.git
cd ride-list-api
```


### Prerequisites

- Python 3.12
- psql 17.4


### Installation


- Run this on terminal

```bash

# Create and activate the virtual environment:
python -m venv venv
source venv/bin/activate # for linux. On Windows, use venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from .env.sample (included the default values for easy setup of local db)
cp .env.sample .env

# Setup the database
bash setup_db.sh

# Run migrations
python manage.py migrate

# Create Django superuser non-interactively
echo "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'Admin1234@')
    admin.role = 'admin'
    admin.save()
" | python manage.py shell

# Populate the database with sample data
python populate_db.py

# Run the dev server
python manage.py runserver 8082


```

### Access the API

Once the server is running:
- Open your browser and go to: http://127.0.0.1:8082

- Access the Django admin panel at: http://127.0.0.1:8082/admin

    - Login using:

        - Username: admin

        - Password: Admin1234@

- View the Ride List API at: http://127.0.0.1:8082/api/rides/
