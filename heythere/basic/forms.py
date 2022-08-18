from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper


class PostForm(forms.ModelForm):
    caption = forms.CharField(widget=forms.Textarea(attrs={"rows":5, 'placeholder': 'whats on your mind...'}))
    image = forms.FileField(widget=forms.FileInput(attrs={'name':'inpFile', 'id':'inpFile'}))

    class Meta:
        model = Post
        fields = '__all__'
        Widgets = {
            'caption' : forms.Textarea(attrs={'placeholder':'caption'}),
            'image' : forms.FileInput(attrs={'class':'form-control'}),
            'local_visibility' : forms.Select(attrs={'class':'form-control'}),
            'global_visibility' : forms.Select(attrs={'class':'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['caption'].label = False
        self.fields['image'].label = False
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
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Circle title...'}))
    circle_creator = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','disabled':True}))
    neighbourhood = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','disabled':True}))
    image = forms.FileField(widget=forms.FileInput(attrs={'name':'inpFile', 'id':'inpFile'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":3, 'placeholder': 'Circle description...'}))

    class Meta:
        model = Circle
        fields = ['name','description','circle_creator','image','neighbourhood','members']

        Widgets = {
            'circle_creator' : forms.TextInput(attrs={'class':'input disabled'}),
        }

    def __init__(self, *args, **kwargs):
        super(CircleForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = False
        self.fields['description'].label = False
        self.fields['image'].label = False


    