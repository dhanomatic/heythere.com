from email.policy import default
from pyexpat import model
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
    creator = models.ForeignKey(UserRegister, on_delete=models.CASCADE, null=True, related_name='creator')
    caption = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    date_update = models.DateTimeField(auto_now=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked', null=True, blank=True)

    class Meta:
        ordering = ['-date_update','-date_create']

    def __str__(self):
        return self.creator.username

    @property
    def total_like(self):
        return self.likes.all().count()

LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE, null=True)
    body = models.TextField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    date_update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self) :
        return '%s - %s' %(self.post.caption, self.name)

