from django.db import models
from datetime import date

class Room(models.Model):
    name = models.CharField(max_length=128)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=True)

class Reservation(models.Model):
    date = models.DateField()
    comment = models.TextField()
    reserve = models.ForeignKey(Room, on_delete=models.CASCADE)