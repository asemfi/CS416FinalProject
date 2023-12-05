from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=12)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
