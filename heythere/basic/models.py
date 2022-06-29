from email.policy import default
from tkinter import CASCADE
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Neighbourhood(models.Model):
    neighbourhood = models.CharField(max_length=100)

    def __str__(self):
        return self.neighbourhood

class UserRegister(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, null=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username

class Post(models.Model):
    creator = models.ForeignKey(UserRegister, on_delete=models.CASCADE, null=True)
    caption = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    date_update = models.DateTimeField(auto_now=True, null=True)
    upvote = models.IntegerField( null=True, blank=True)
    downvote = models.IntegerField( null=True, blank=True)

    class Meta:
        ordering = ['-date_update','-date_create']

    def __str__(self):
        return self.creator.username

class VoteStatus(models.Model):
    userid = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    postid = models.ForeignKey(Post, on_delete=models.CASCADE)
    upvotestatus = models.BooleanField(default=False)
    downvotestatus = models.BooleanField(default=False)