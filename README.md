# GEO
Installation
1. Clone the Repository
git clone <your-repo-url>
cd geoshop

2. Docker Setup

Make sure you have Docker and Docker Compose installed.

3. Build and Run Containers
docker-compose up --build


This will:

Build the Docker image for your Django app.

Start a PostGIS database container.

Run Django migrations automatically.

Start the Django development server at http://localhost:8000
.

Database Migration

The database migration is already handled in the docker-compose.yaml command:

command: >
  sh -c "python manage.py migrate &&
         python manage.py runserver 0.0.0.0:8000"


If you want to manually run migrations inside the container:

docker-compose run web python manage.py migrate


Starting the Server

Once the containers are running, open your browser:

http://localhost:8000




Commands Cheat Sheet

Build and run containers:

docker-compose up --build


Run migrations manually:

docker-compose run web python manage.py migrate


Create superuser:

docker-compose run web python manage.py createsuperuser


Stop containers:

docker-compose down





Folder Structure
backend/
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── geoshop/           # Django project
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── shops/             # Django app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   └── templates/
└── ...