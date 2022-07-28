from datetime import date
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
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
    image = models.ImageField(null=True, blank=True)
    friends =  models.ManyToManyField('self', related_name='friends', blank=True)

    def get_friends(self):
        return self.friends.all()

    def get_friends_count(self):
        return self.friends.all().count()


    def __str__(self):
        today = date.today()
        delta = relativedelta(today, self.dob)
        return str(delta.years)

    def __str__(self):
        return self.username

    @property
    def imageURL(self):
        try:
            url = self.image.url

        except:
            url = ''
        return url


STATUS_CHOICES = (
    ('none', 'none'),
    ('send', 'send'),
    ('accepted', 'accepted'),
    ('decline', 'decline'),
)
class Friend(models.Model):
    sender = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    receiver = models.ForeignKey(UserRegister, on_delete=models.CASCADE, related_name='receiver', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='none', null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

class Circle(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    circle_creator = models.ForeignKey(UserRegister, on_delete=models.DO_NOTHING, related_name='circle_creator', null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    neighbourhood = models.CharField(max_length=100, null=True, blank=True)
    members = models.ManyToManyField(UserRegister, related_name='members', null=True, blank=True)

    class Meta:
        ordering = ['-date_create']

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url

        except:
            url = ''
        return url



class Join(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    Join_CHOICES = (
        ('Join', 'Join'),
        ('Leave', 'Leave'),
    )
    value = models.CharField(choices=Join_CHOICES, default='Join', max_length=10)

    def __str__(self):
        return str(self.circle)


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
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE, related_name='circle', null=True, blank=True)

    class Meta:
        ordering = ['-date_create']

    # def __str__(self):
    #     return self.creator.username
    @property
    def imageURL(self):
        try:
            url = self.image.url

        except:
            url = ''
        return url

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



    
