# This application requires to be run with docker-compose. running the Dockerfile by its own won't work.

FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
# Because a container has its own lo interface, 127.0.0.1 can only be used from within the container.
# 0.0.0.0 is an “all interfaces” address, which will also accept connections from the container interface that connects to the outside.
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
