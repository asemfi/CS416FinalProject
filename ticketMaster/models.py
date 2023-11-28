from django.db import models

# Create your models here.


class Event(models.Model):
    eventID = models.CharField(max_length=20, unique=True)
    eventName = models.CharField(max_length=200)
    localDateTime = models.DateTimeField()
    venue = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    imageLink = models.CharField(max_length=200)

    def __str__(self):
        return self.eventID


class Comments(models.Model):
    eventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    starRating = models.IntegerField()
    comment = models.CharField(max_length=2000)