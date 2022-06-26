from tkinter import CASCADE
from tkinter.tix import Tree
from django.db import models

# Create your models here.

class Neighbourhood(models.Model):
    neighbourhood = models.CharField(max_length=100)

class UserRegister(models.Model):
    username = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, null=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)

class Post(models.Model):
    creator = models.ForeignKey(UserRegister, on_delete=models.CASCADE, null=True)
    caption = models.TextField(max_length=500, null=True)
    image = models.ImageField()
    date_create = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now_add=True)
    upvote = models.IntegerField()
    downvote = models.IntegerField()

class VoteStatus(models.Model):
    userid = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    postid = models.ForeignKey(Post, on_delete=models.CASCADE)
    upvotestatus = models.BooleanField(default=False)
    downvotestatus = models.BooleanField(default=False)