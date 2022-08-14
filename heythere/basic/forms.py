from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        Widgets = {
            'caption' : forms.Textarea(attrs={'rows':6, 'cols':4}),
            'image' : forms.FileInput(attrs={'class':'form-control'}),
            'local_visibility' : forms.Select(attrs={'class':'form-control'}),
            'global_visibility' : forms.Select(attrs={'class':'form-control'}),
        }
        # fields = ['creator','caption', 'image', 'local_visibility', 'global_visibility']

class CreateUserForm(UserCreationForm):
    neighbourhood = forms.ModelMultipleChoiceField(queryset=Neighbourhood.objects.all())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','neighbourhood']

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = UserRegister
        fields = ['neighbourhood']
        # fields = '__all__'

class UserRegisterForm2(forms.ModelForm):
    class Meta:
        model = UserRegister
        # fields = ['neighbourhood']
        fields = '__all__'


class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":3, 'placeholder': 'write a comment...'}))
   
    class Meta:
        model = Comment
        fields = ('post','user', 'body')

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


class CircleForm(forms.ModelForm):
    class Meta:
        model = Circle
        fields = '__all__'