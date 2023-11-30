from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# User is an object that correlates to rows of the auth_user table

# User is an object that correlates to rows of the auth_user table

# User is an object that correlates to rows of the auth_user table

# Create your models here.


class Event(models.Model):
    eventID = models.CharField(max_length=20, primary_key=True, unique=True)
    eventName = models.CharField(max_length=200)
    localDateTime = models.DateTimeField()
    venue = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    imageLink = models.CharField(max_length=200)

    def __str__(self):
        return self.eventID


class Comments(models.Model):
    eventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    starRating = models.IntegerField(default='-1', editable=False)
    comment = models.CharField(max_length=2000)

    def __str__(self):
        return self.comment


class SavedEvents(models.Model):
    eventID = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)



# makemigrations ticketMaster
# migrate ticketMaster