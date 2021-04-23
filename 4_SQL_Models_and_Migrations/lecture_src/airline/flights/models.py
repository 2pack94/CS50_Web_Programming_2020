from django.db import models

# Create your models here.
# Models: https://docs.djangoproject.com/en/3.1/topics/db/models/
# Model Fields: https://docs.djangoproject.com/en/3.1/ref/models/fields/
# By default, Django gives each model an auto-incrementing primary key (PK) field with the name "id".

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    # The columns origin and destination contain foreign keys that refer to the PK of the Airport table.
    # CASCADE: if the related object (Airport) is deleted,
    # delete also all objects from this table (flights) that refer to this Airport.
    # related_name: The name to use for the relation from the related object back to this one.
    # An Airport instance can use the name "departures" to get all flights that have this Airport as origin.
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id} : {self.origin} to {self.destination}"


class Passenger(models.Model):
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    # many-to-many relationship between passengers and flights
    # Django will create a join table with the 3 columns: id, passenger_id, flight_id
    flights = models.ManyToManyField(Flight, blank=True, related_name="passengers")

    def __str__(self):
        return f"{self.first} {self.last}"
