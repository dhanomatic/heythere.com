from pyexpat import model
from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    neighbourhood = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-date']

class Message(models.Model):
    value = models.CharField(max_length=10000000)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.CharField(max_length=100)
    room = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date']

class ActiveUsers(models.Model):
    username = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.username