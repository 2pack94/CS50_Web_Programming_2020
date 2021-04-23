This projects demonstrates:
    Github Actions: in .github/workflows/ci.yml
    Docker and Docker Compose: in docker-compose.yml
    Django unit testing: in flights/tests.py

The Django Project is set-up to use a postgreSQL database (see: settings.py).
The docker-compose.yml file sets up a container running the database server and a container running the Django backend.
Django communicates with the postgres Server via the configured settings.
