from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=1000)

class Message(models.Model):
    value = models.CharField(max_length=10000000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=100)