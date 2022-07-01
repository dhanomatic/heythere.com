from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    neighbourhood = forms.ModelMultipleChoiceField(queryset=Neighbourhood.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','neighbourhood']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'