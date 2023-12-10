from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# User is an object that correlates to rows of the auth_user table

# Create your models here.


class Event(models.Model):
    event_id = models.CharField(max_length=20, unique=True)
    eventName = models.CharField(max_length=200, null=True)
    eventLink = models.CharField(max_length=300, null=True)
    imageLink = models.CharField(max_length=300, null=True)
    venue = models.CharField(max_length=200, null=True)
    localDate = models.DateField(null=True)
    localTime = models.TimeField(null=True)
    address = models.CharField(max_length=200)
    cityState = models.CharField(max_length=200, null=True)
    googleMap = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.event_id


class Comment(models.Model):
    eventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    starRating = models.IntegerField(default=-1, editable=True, validators=[
            MaxValueValidator(5),
            MinValueValidator(-1)
        ])
    comment = models.CharField(max_length=2000)

    def __str__(self):
        return self.comment


class SavedEvent(models.Model):
    eventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)



# makemigrations ticketMaster
# migrate ticketMaster