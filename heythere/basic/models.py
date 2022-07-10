from datetime import date
from email.policy import default
from enum import unique
from pyexpat import model
from tkinter import CASCADE
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import User
from django.forms import BooleanField
from phone_field import PhoneField
from dateutil.relativedelta import relativedelta

# Create your models here.

class Neighbourhood(models.Model):
    neighbourhood = models.CharField(max_length=100)

    def __str__(self):
        return self.neighbourhood

class UserRegister(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, null=True)
    fname = models.CharField(max_length=100, null=True, blank=True)
    lname = models.CharField(max_length=100, null=True, blank=True)
    # neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, null=True)
    neighbourhood = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phonenumber = PhoneField(null=True, blank=True, help_text='Contact phone number')
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    bio = models.CharField(max_length=50, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    dob = models.DateField(max_length=8, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True) 
    propic = models.ImageField(null=True, blank=True)
    def __str__(self):
        today = date.today()
        delta = relativedelta(today, self.dob)
        return str(delta.years)

    def __str__(self):
        return self.username

class Post(models.Model):
    creator = models.ForeignKey(UserRegister, on_delete=models.CASCADE, null=True, related_name='creator')
    caption = models.TextField(max_length=500, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    local_visibility = models.BooleanField(default=True, null=True, blank=True)
    global_visibility = models.BooleanField(default=False, null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    date_update = models.DateTimeField(auto_now=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked', null=True, blank=True)
    commets = models.ManyToManyField(User, related_name='commented', null=True, blank=True)

    class Meta:
        ordering = ['-date_create']

    # def __str__(self):
    #     return self.creator.username

    @property
    def total_like(self):
        return self.likes.all().count()

    @property
    def total_like(self):
        return self.commets.all().count()

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
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='user_comment', on_delete=models.CASCADE, null=True)
    body = models.TextField(verbose_name="comment", null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True, null=True)
    date_update = models.DateTimeField(auto_now=True, null=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+') # '+' take away reverse mapping

    class Meta:
        ordering = ['-date_create']

    # def __str__(self) :
    #     return '%s - %s' %(self.post.caption, self.user.username)

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-date_create').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False


